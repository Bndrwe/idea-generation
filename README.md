# idea-generation

A Claude skill for brainstorming ideas that are unusual and still workable: side projects, small businesses, fundraisers, stories, startups. It works by first listing the ideas any chatbot would give, banning them, generating from structured prompts, and then running every idea past a skeptical judge before anything reaches you.

## Why AI ideas all sound the same

Ask three chatbots for side-project ideas and you get the same ten answers. Research points to a few causes:

- Preference training flattens the output. RLHF cuts output diversity compared with fine-tuning alone ([Kirk et al., ICLR 2024](https://arxiv.org/abs/2310.06452)). Human raters prefer familiar, typical text, so the reward pushes models toward the most stereotypical answer ([Zhang et al. 2025, Verbalized Sampling](https://arxiv.org/abs/2510.01171)). Base models beat their aligned versions on randomness and creativity tasks ([West and Potts 2025](https://arxiv.org/abs/2505.00047)).
- Different models give the same answers. LLM answers to creativity tests look much more like each other than human answers do ([Wenger and Kenett 2025](https://arxiv.org/abs/2501.19361)). Across 26,000 open-ended prompts, different models produced strikingly similar outputs, which the authors call the "Artificial Hivemind" ([Jiang et al., NeurIPS 2025](https://arxiv.org/abs/2510.22954)). Switching apps doesn't help.
- Idea lists run dry fast. GPT-4 idea pools were less diverse than pools from groups of people, and unique ideas got used up quickly ([Meincke, Mollick and Terwiesch 2024](https://arxiv.org/abs/2402.01727)). When thousands of research ideas were generated, most were duplicates ([Si, Yang and Hashimoto 2024](https://arxiv.org/abs/2409.04109)).
- Temperature isn't a creativity dial. It barely tracks novelty and does track incoherence ([Peeperkorn et al., ICCC 2024](https://arxiv.org/abs/2405.00492)).
- The judge has the same bias. LLM evaluators recognize and favor their own output ([Panickssery et al., NeurIPS 2024](https://arxiv.org/abs/2404.13076)), so a model scoring its own ideas drifts back toward the typical ones.

## What the skill does about it

1. It pins down the brief: who it's for, skills, budget, time, limits. If you say "just go", it assumes and lists its assumptions.
2. It writes a cliché wall. It starts with the exact list it would give with no skill, then adds the other ideas any AI would give, plus "clever-sounding defaults" like "AI-powered X" or "a marketplace for Y". Nothing later may be a reworded version of these. You can see the wall in a collapsed section.
3. It draws a map of two axes that matter for the brief, such as who pays × how it works. The goal is ideas spread across cells, a version of quality-diversity search ([Bradley et al., ICLR 2024](https://arxiv.org/abs/2310.13032)). Only cells where real people spend money count.
4. It generates ideas with forcing techniques: collision with an unrelated field, inversion, underserved users, extreme constraints, time shifts, scale shifts, annoyance mining and outsider views. Each idea gets a rough probability that a typical AI would suggest it, and common ones are cut ([verbalized sampling](https://arxiv.org/abs/2510.01171)). Then a pass rewrites each idea so it works in a bolder way while keeping the same customers ([Meincke et al.](https://arxiv.org/abs/2402.01727)).
5. It switches to a skeptical judge. The ideas are rewritten as a bare list with no labels or reasoning and judged as if someone else wrote them. If subagents are available, a separate one does this. Checks: typicality, originality, reality (including licenses and liability), fit, demand with rough numbers against your goal, and a red-team case.
6. It shortlists across the map. A finalist needs Feasibility 4+ and Demand 3+; novelty breaks ties. Each finalist gets one more check against the cliché wall. You also get one line naming the safest obvious option, so you can weigh the odd ideas against the proven one.
7. It shows its work: the map, finalists with the hardest part, the red-team case and a first step that takes under a week, and a table of dropped ideas so you can rescue anything cut too harshly.

The skill names no example fields or jobs on purpose (see the test results for why).

## Install

**Claude.ai / Claude desktop:** download `idea-generation/SKILL.md`, zip the `idea-generation` folder, and upload it in the Skills section of Claude's settings.

**Claude Code:** copy the folder into your skills directory:

```bash
git clone https://github.com/bndrwe/idea-generation
cp -r idea-generation/idea-generation ~/.claude/skills/
```

Then ask for ideas as normal ("give me side project ideas, I have 5 hours a week"). The skill triggers on brainstorming requests.

## Test results

I tested it on three ordinary briefs: a side project for a solo developer with 5 hours a week, a small business for a retired nurse with $10k, and a $3,000 fundraiser for a high school robotics club. Each brief ran twice with no skill, with the first version of the skill (v1), with a research-based rewrite (v2), and with this version. A fresh model, blind to which version wrote what, grouped duplicate ideas, flagged ones that matched a plain list of obvious answers, and rated workability from 1 to 5.

| | No skill | v1 | v2 | This version |
|---|---|---|---|---|
| Final picks matching the obvious list | 23 of 30 | 9 of 30 | 2 of 30 | 3 of 28 |
| Same idea in both runs | 9 | 6 | 2 | 6 |
| Workability (1-5) | 3.7 | 3.1 | 3.1 | 3.3 |

What the tests changed:

- The skill's own examples became the new cliché. v1 and v2 listed sample fields for the collision technique (beekeeping, maritime law, geology and so on). Those words showed up in 10 of 12 runs, including a beehive voice log as a *software* side project. This version names no examples and has the model list ten unrelated fields and use the last three. The leak went to 0 of 6 runs.
- An obvious idea won. v2 ranked "mobile foot care nurse" first, which the plain model also suggests. Finalists now get a last check against the cliché wall.
- Workability dropped. Unusual ideas are harder to pull off. The strict feasibility and demand bar and the demand math brought it back up to 3.3, and the "safest obvious option" line keeps the proven choice on the table.

Caveats: two runs per brief and one judge, so read the numbers as a direction. The stricter bar also makes runs agree more often (6 repeats). The skill still has a few favorite ideas of its own, like a corporate robot-building night for the robotics club.

## Example output

Brief: *"Our high school robotics club needs to raise about $3,000 for competition fees. Give us fundraiser ideas. Just go, don't ask questions."*

With no skill, both runs gave the same list: business sponsorships, a kids' STEM camp, a robot demo booth, crowdfunding, restaurant spirit nights.

With the skill (trimmed):

> **Obvious ideas (skipped):** car wash, bake sale, sponsorship letters, GoFundMe, restaurant spirit nights, raffle, t-shirts, cookie-dough sales, summer robotics camp, robot demo with a donation jar, 3D-printed keychains, trivia night, can drive. *Clever-sounding defaults:* AI tutoring service, marketplace for student 3D prints, gamified donation leaderboard, STEM subscription box, maker community app.
>
> **Safest obvious option:** sponsorship tiers for local businesses ($100, $250 or $500 for a logo on the robot and banner). It's proven, and it pairs well with any idea below.
>
> **1. Gift Assembly Depot.** Parents drop off boxed bikes, playhouses and trampolines at school. The team assembles them and stores them out of sight until pickup on Dec 22-23.
> - Twist: home assemblers charge $60-100 an hour and come to your house. This is cheaper, and it hides the gifts from your kids.
> - Hardest part: secure storage and damage liability. Needs school approval, a signed waiver, intake photos and a locked room.
> - Red team: "Parents won't hand gifts to teenagers." Answer: the advisor supervises, and it's pitched to families who already know the school.
> - Math: about 40 jobs at an average of $55 comes to about $2,200.
> - Scores: Novelty 4, Feasibility 4, Demand 4. First step: get a storage room signed off and post a pricing flyer to the parent list this week.
>
> **2. Office Robot League.** Local companies pay $400 a team to build and battle kit robots over three evenings, coached by students.
>
> **3. Saturday Sharpening Bench.** Walk-up knife, scissor and garden-tool sharpening at holiday markets for $7 each. Math: 60-100 items a market day comes to $400-700, so four or five days bring in about $2,000.
>
> **4. Animated Shop Windows.** Rent simple moving holiday window displays to downtown shops for $250 a season, with a "Built by [School] Robotics" sign.
>
> **Dropped:** wedding cake toppers (Etsy undercuts it), fix-it clinic (Repair Café exists), broken-toy hospital ($10 tickets can't reach $3,000), middle school scrimmage (a standard move for FIRST teams), senior tech help (on every AI list), laser engraving (needs a laser over budget).

## License

MIT. See [LICENSE](LICENSE).
