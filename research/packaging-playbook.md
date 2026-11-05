# Packaging & retention playbook (2026-11-05)

Two evidence sources, weighted accordingly:

1. **Our own measurement (strongest).** 1,941 videos from 19 data-story channels (Spreadsheet Sports,
   HQE, BlitzTalk, Newbie Indie Game Dev, Astroid, Data Time, Ioana Roman, Water CS2, Wilytics,
   Gym Leader Matt, RealityMargin, …). Each video's views are divided by **its own channel's median**,
   which controls for channel size. The 3 newest videos per channel are excluded because their views
   are still accruing. Code: `tools/title_feature_analysis.py`; data: `raw/cohort_videos.json`.
   These are correlations, not experiments.
2. **YouTube's own documentation** (reliable) and the creator-industry consensus (directional; most 2026
   "CTR +30%" stats are unsourced vendor-blog numbers, so they are not repeated here).

---

## 1. The idea is the packaging
The outliers are not won by thumbnail polish. They are won by **an idea a stranger understands and
wants answered in under a second**:

| Outlier | x channel median |
|---|---|
| I Built a Model to Find the Most Average NBA Player | 5,800x |
| I Scraped the Entire Steam Catalog, Here's the Data | 162x |
| I Simulated 1,810,053 Battles to Find the Strongest Pokémon | 155x |
| I analyzed all words on the Mr Beast channel | 120x |
| I Built a Model to Find the Unluckiest Team in the NFL | 98x |
| I Analysed 47,000 Games of Catan. Here's How to Win Every Time | 33x |

Pattern: **[huge, universally known subject] + [one extreme superlative or answer] + [proof of effort]**.

Losers (0.0-0.1x): team-specific or local-interest topics ("The Angels Are Hilariously Bad",
"The Pirates are good??"), time-bound takes, documentaries and film breakdowns.

**Rule:** before scripting anything, write the title and thumbnail first. If the idea doesn't excite
someone who isn't a fan of a specific team or game, don't make it.
Games filter: the subject must be bigger than one game's fanbase (all of Steam, every console, every
GOTY winner), or it must be one of the very biggest games.

## 2. Titles: what the data says
| Title feature | n | median x (with) | median x (without) |
|---|---|---|---|
| Big specific number (≥1,000: "1,810,053 battles", "47,000 games") | 36 | **1.70** | 1.00 |
| First-person "I …" ("I Built / I Simulated / I Analyzed") | 164 | **1.56** | 1.00 |
| "Here's what I found / Here's the data" | 10 | 1.54 | 1.00 |
| Superlative (most/best/worst/-est/ever) | 202 | **1.24** | 1.00 |
| Model/simulation/data words | 133 | 1.08 | 1.00 |
| Question mark | 321 | 0.95 | 1.00 |
| Year in the title | 87 | **0.72** | 1.00 |
| Parentheses/brackets ("(Film Breakdown)", "(Documentary)") | 127 | **0.53** | 1.01 |

Title template (use one or two of these, not all):
- `I Built a Model to Find the {Superlative} {Subject} Ever`
- `I Analyzed {Big Exact Number} {Things}. Here's What I Found.`
- `I Simulated {Thing} {Big Number} Times`
- `{Bold claim}. I Ran the Numbers.`

Do:
- Keep it under ~60 characters so it isn't truncated on mobile.
- Use exact, odd numbers (1,810,053 beats "1.8 million").
- Name a famous subject.
- Write a claim, not a question.

Don't:
- Put a year in an evergreen title.
- Add series labels in parentheses.
- Lean on question marks or ALL-CAPS.

## 3. Thumbnails: top-20 vs bottom-20 comparison
Contact sheets: `img/thumbs_top.jpg` and `img/thumbs_bottom.jpg`.

**Winners:**
- **One dominant subject**, large, on a clean or simple background.
- **0-3 words of text**, and the text adds to the title instead of repeating it ("DEAD LAST",
  "Here it is", "I analyzed his words").
- **The data visual is the thumbnail.** BlitzTalk's 98x outlier is a black scatter plot with a single
  red-circled dot and an arrow: "which one is it?" This is native to our style and fully generatable.
- **Instantly recognizable icons:** a famous face, a famous logo or character, or a recognizable
  game's key art.
- **Social proof:** Newbie Indie Game Dev's 162x thumbnail is a screenshot of a viewer comment over the data.
- **Curiosity marker:** an arrow or circle pointing at the answer without revealing it.

**Losers:**
- Collages of 3-5 people.
- Headline text repeating the title, often as a question ("THE PIRATES ARE GOOD??").
- Busy stock action photos.
- Small-audience subjects.

**Our thumbnail system:**
1. A dark background with one bold chart (a scatter, ranking bar or curve) and one highlighted mark.
2. One hero element: a game's cover/key art or a famous icon, cut out and large.
3. At most 3 words in a heavy font, high contrast, readable at 160 px wide.
4. Hide the answer: blur it, use "???", or point an arrow at it.
5. Make 3 variants per video for YouTube's Test & Compare (below).
6. Before publishing, check every thumbnail at mobile size (~160x90) next to competitors in a mock search grid.

## 4. Length and structure for retention
| Duration | median x | share ≥2x |
|---|---|---|
| < 5 min | 0.53 | 17% |
| 5-10 min | 1.00 | 29% |
| **10-15 min** | **1.15** | **32%** |
| 15-20 min | 1.07 | 28% |
| 20-30 min | 0.93 | 21% |
| 30+ min | 0.99 | 20% |

**Target 10-14 minutes.** The reference channel's hits sit at 8-15 minutes.

YouTube's Key Moments report treats the first 30 seconds ("Intro") as the main drop-off. The leaked
MrBeast production guide frames every decision around retention: the first minute is where most
viewers are lost, and the video must deliver what the thumbnail promised.

**Script skeleton for a data-story video:**

| Time | Beat | Purpose |
|---|---|---|
| 0:00-0:15 | **Cold open.** State the claim and show the thumbnail's chart. "I ranked all 84,000 games on Steam, and the most underrated one has fewer reviews than a Minecraft mod." | Confirms the click was worth it, with no intro and no "subscribe". |
| 0:15-0:45 | **Stakes and method in one breath.** What "underrated" means and the dataset size, shown visually. | Credibility without a lecture. |
| 0:45-1:00 | **Open loop.** "Number one surprised me, but first: the games everyone thinks are underrated, and why they aren't." | A reason to stay. |
| 1:00-10:00 | **Countdown or escalating reveals.** Each segment lasts 60-90 s and ends on a mini-cliffhanger, with a visual change every 3-6 s. Include a "the model is wrong?" twist around the midpoint. | Rehooks against mid-video drop-off. |
| 10:00-11:30 | **The payoff (#1).** It must match the thumbnail promise. | Satisfaction, which drives watch time and recommendations. |
| 11:30-12:00 | **Hand-off.** Name the next debate and link the companion site and the next video. Never say "that's it for today". | Session time and the end-screen click. |

Production rules:
- **Script the narration in short spoken sentences** (synthetic voices sound best that way).
- **Every number on screen is animated.** No static slides longer than ~6 s.
- **Chapters** need a first timestamp at 0:00 and at least 3 chapters; they appear as "key moments"
  in Google Search. Use them, but name them like curiosity hooks, not a table of contents.

## 5. Description, tags and metadata
YouTube says the title, description and spoken transcript matter, while tags play a "limited role",
mostly catching misspellings. So:
- **Description:** 1-2 natural sentences restating the question and the answer domain (the first ~150
  characters show in search). Then the chapters, a sources and method line (builds trust; our edge), a
  link to the companion site, and 2-3 related videos.
- **Tags:** 5-10 terms covering misspellings and variants (`steam`, `underrated games`,
  `hidden gems steam`, …), then move on.
- **Hashtags:** at most 3 (YouTube shows the first 3 above the title).
- **Transcript:** say the key phrases out loud (e.g. "most underrated game on Steam"), since speech is indexed.

## 6. Testing (Test & Compare)
YouTube Studio's native test runs **up to 3 titles and/or thumbnails** and picks the winner by
**watch time, not CTR**, within about 2 weeks. Editing the title or thumbnail mid-test stops it.
Because watch time decides, a clickbait thumbnail that disappoints viewers loses automatically.
**Run a test on every upload**; we can generate variants automatically.

## 7. Engagement
There is no rigorous public evidence on pinned comments or calls to action. Practical defaults:
- **Pinned comment:** ask a specific debate question ("Which game did the model miss?") plus the site link.
- **The model invites argument.** "Tell me what to model next" (as the reference channel does) turns
  comments into a topic pipeline. Answer early comments in the first hour.
- **Companion site:** viewers look up their favorite game's score. This drives comments ("my game
  is #4,312??") and return visits.

## 8. Automated pipeline checklist (per video)
1. Generate 20 title and premise ideas, score them against sections 1-2, and pick one.
2. Build the model, then find the most surprising true result. The result chooses the story, not the reverse.
3. Script with the section-4 skeleton (target ~1,600-1,900 spoken words for 11-13 min).
4. Generate the voiceover, then render the video timed to the voice.
5. Produce 3 thumbnails and 3 titles; check them at mobile size.
6. Write the description (section 5), chapters, pinned comment and end screen.
7. After publishing, read the CTR, average-view-duration and retention curve at 48 h and 7 d, and
   feed the drop-off points back into the script template.
