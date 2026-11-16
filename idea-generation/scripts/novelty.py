#!/usr/bin/env python3
"""Vector novelty check for the idea-generation skill.

Embeds the cliche wall (the obvious ideas) and the candidate ideas with a small
local model, then reports how far each candidate sits from the crowded region.
No API key. Runs on CPU.

Usage:
  python3 novelty.py obvious.txt candidates.txt

Each file holds one idea per line ("Name: one-line pitch"). Blank lines and
lines starting with # are ignored.

Exit code 0 = report printed. Exit code 3 = no embedding backend available;
the skill then falls back to the word-based typicality check.

Backends, tried in order:
  1. sentence-transformers with all-MiniLM-L6-v2  (pip install sentence-transformers)
  2. the same model as ONNX via onnxruntime + tokenizers
     (pip install onnxruntime tokenizers numpy). Model files are fetched once
     (~80 MB) into ~/.cache/idea-generation/ unless IDEA_EMBED_MODEL_DIR points
     to a folder that already has model.onnx and tokenizer.json.
"""
import os, sys, tarfile, urllib.request

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
ONNX_URL = "https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz"
CACHE = os.path.expanduser("~/.cache/idea-generation")


def read(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip().lstrip("-*0123456789. ").strip() for l in f
                if l.strip() and not l.lstrip().startswith("#")]


def embed_st(texts):
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(MODEL)
    return m.encode(texts, normalize_embeddings=True)


def onnx_dir():
    d = os.environ.get("IDEA_EMBED_MODEL_DIR")
    if d:
        return d
    d = os.path.join(CACHE, "onnx")
    if not os.path.exists(os.path.join(d, "model.onnx")):
        os.makedirs(CACHE, exist_ok=True)
        tgz = os.path.join(CACHE, "onnx.tar.gz")
        urllib.request.urlretrieve(ONNX_URL, tgz)
        with tarfile.open(tgz) as t:
            t.extractall(CACHE, filter="data") if hasattr(tarfile, "data_filter") else t.extractall(CACHE)
        os.remove(tgz)
    return d


def embed_onnx(texts):
    import numpy as np, onnxruntime as ort
    from tokenizers import Tokenizer
    d = onnx_dir()
    tok = Tokenizer.from_file(os.path.join(d, "tokenizer.json"))
    tok.enable_truncation(max_length=256)
    tok.enable_padding(pad_id=0, pad_token="[PAD]")
    sess = ort.InferenceSession(os.path.join(d, "model.onnx"), providers=["CPUExecutionProvider"])
    enc = tok.encode_batch(texts)
    ids = np.array([e.ids for e in enc], dtype=np.int64)
    mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
    feeds = {"input_ids": ids, "attention_mask": mask}
    if "token_type_ids" in [i.name for i in sess.get_inputs()]:
        feeds["token_type_ids"] = np.zeros_like(ids)
    out = sess.run(None, feeds)[0]
    m = mask[..., None].astype(np.float32)
    v = (out * m).sum(1) / m.sum(1)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def embed(texts):
    errors = []
    for fn in (embed_st, embed_onnx):
        try:
            return fn(texts), fn.__name__[6:]
        except Exception as e:  # missing package, no network, etc.
            errors.append(f"{fn.__name__[6:]}: {type(e).__name__}: {e}")
    print("NO_EMBEDDINGS: fall back to the word-based typicality check.", file=sys.stderr)
    for e in errors:
        print("  " + e, file=sys.stderr)
    sys.exit(3)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    import numpy as np
    wall, cands = read(sys.argv[1]), read(sys.argv[2])
    if len(wall) < 5 or not cands:
        sys.exit("Need at least 5 obvious ideas and 1 candidate.")
    V, backend = embed(wall + cands)
    W, C = V[:len(wall)], V[len(wall):]

    # How tightly packed is the wall? Each obvious idea's nearest other obvious idea.
    S_ww = W @ W.T
    np.fill_diagonal(S_ww, -1)
    nn_wall = S_ww.max(1)
    radius = float(np.median(nn_wall))  # "as close as obvious ideas are to each other"
    centroid = W.mean(0); centroid /= np.linalg.norm(centroid)
    cw = W @ centroid
    cmu, csd = float(cw.mean()), float(cw.std()) or 1e-6

    S_cw = C @ W.T
    near = S_cw.argmax(1)
    S_cc = C @ C.T
    np.fill_diagonal(S_cc, -1)

    print(f"backend: {backend} | {len(wall)} obvious, {len(cands)} candidates")
    print(f"crowded-zone radius (median obvious-to-obvious similarity): {radius:.2f}")
    print("Verdicts: INSIDE = as close to an obvious idea as obvious ideas are to each other;"
          " EDGE = within 0.08 of that; OUT = clear of the crowded zone.\n")
    rows = []
    for i, c in enumerate(cands):
        s = float(S_cw[i, near[i]])
        z = (float(C[i] @ centroid) - cmu) / csd
        verdict = "INSIDE" if s >= radius else "EDGE" if s >= radius - 0.08 else "OUT"
        rows.append((s, i, verdict, z))
    for s, i, verdict, z in sorted(rows, reverse=True):
        print(f"[{verdict:6}] sim {s:.2f} | centre z {z:+.1f} | {cands[i][:90]}")
        print(f"          nearest obvious: {wall[near[i]][:90]}")

    dups = [(float(S_cc[i, j]), i, j) for i in range(len(cands)) for j in range(i + 1, len(cands))
            if S_cc[i, j] >= max(radius, 0.6)]
    if dups:
        print("\nNear-duplicate candidates (merge or keep one):")
        for s, i, j in sorted(dups, reverse=True):
            print(f"  {s:.2f}  {cands[i][:60]}  <->  {cands[j][:60]}")

    # Steering: candidates farthest from the wall and from each other mark open space.
    iso = [(float(S_cw[i].max()) + max(float(S_cc[i].max()), 0) , i) for i in range(len(cands))]
    print("\nMost open directions (far from the wall and from other candidates):")
    for s, i in sorted(iso)[:3]:
        print(f"  {cands[i][:100]}")


if __name__ == "__main__":
    main()
