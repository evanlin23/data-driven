# Making it not feel AI-made: script, pacing, visuals (2026-11-05)

Why it matters:
- YouTube's monetization rule targets *inauthentic*, mass-produced, repetitive content, not AI
  tools themselves.
- Viewers bail on "AI slop" from the generic phrasing, the generic visuals, and the sense that
  nobody in particular made the video for anybody in particular.
- Our protection is the same thing that makes the channel good: **original analysis that nobody
  else has, told with a specific point of view.**

Evidence base:
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
  the most rigorous public catalogue, Oct 2026 revision.
- Creator and agency write-ups (directional only).
- Our own cohort data (`packaging-playbook.md`).
- Transcripts of 25 top and 10 bottom videos (`transcript_video_ids.txt`), used to measure
  the real pacing of hits (section 3).

Enforcement: **`pipeline/script_lint.py`**. Every script must PASS before it goes to the voice
model. It hard-bans AI vocabulary, significance puffery, chatbot residue and YouTube clichés. It
also scores soft tells: "not X, it's Y" parallelisms, ", highlighting…" tails, vague attributions,
rule-of-three lists, dash overuse, monotone 8-20-word sentence rhythm, low sentence-length
variation, too many questions, and low specificity (numbers and names per 100 words).

---

## 1. Script: what makes narration read as AI
| Tell | Example | Fix |
|---|---|---|
| Generic significance | "stands as a testament to…", "plays a crucial role" | State the fact plainly: "It sold 40,000 copies." |
| AI vocabulary | delve, tapestry, vibrant, landscape, pivotal, showcase, foster, multifaceted, quietly | Use plain words: "has", "shows", "is". |
| Negative parallelism | "It's not just X, it's Y." "Not X, but Y." "Y rather than X." | Say Y. Use the contrast at most once per video, where it earns it. |
| Dangling analysis | "…, highlighting the challenges indie studios face." | Delete the tail, or replace it with a concrete number. |
| Rule of three | "creativity, passion, and innovation" | Use one precise word, or two. |
| Weasel attribution | "Experts agree…", "Many fans believe…" | Name the source, or cite our own data. |
| Monotone rhythm | Every sentence 12-18 words, every paragraph the same shape | Mix 3-word punches with one long build-up sentence. |
| Fake suspense | "But here's the thing." "The answer might surprise you." | Make the surprising fact itself the hook. |
| Smoothed specifics | "a huge number of games" | "84,302 games" |
| Polite hedging | "based on available data", "it's important to note" | Commit to a claim. Note real caveats once, in plain words. |
| Chatbot frame | "In this video we'll…", "In conclusion…" | Start on the claim and end on the hand-off. |

The Wikipedia guide also notes the reverse: **human writing uses plain copulas** ("is", "has",
"was the first", "is the only"), plain verbs (used / tried / moved), and contractions.

## 2. Script: what makes it sound like a person
- **A narrator with a point of view.** Opinions, small admissions ("I didn't expect this one"),
  jokes at our own model's expense ("the model thinks a farming game should've sold a million
  copies. Stay with me.").
- **Show the work honestly.** Name a dataset limit once ("Steam reviews skew toward people who
  liked the game enough to write one") and move on. Owning the flaws earns trust; hedging every
  sentence is a tell.
- **Specificity everywhere.** Exact numbers, dates, named games, named rivals. The linter wants at
  least 4 numbers or names per 100 words.
- **Write for the ear.** Short sentences, contractions, and no lists read aloud. Numbers rounded
  for speech once the exact figure has appeared on screen ("about forty thousand").
- **Comparisons a gamer feels.** "Fewer reviews than a Counter-Strike skin has trades in an hour",
  not "a statistically low figure".
- **Don't fake disfluency.** Adding "um" and "sooo" to a TTS script makes it sound worse. The
  human feel comes from rhythm and opinion, not filler.
- **Structure from the data.** The most surprising true result picks the order of the story. A
  template that is identical every week is the "repetitive content" YouTube demonetizes. Keep the
  skeleton (hook, method, countdown, payoff) but vary the shape: sometimes a countdown, sometimes
  a mystery ("why did this game fail?"), sometimes a head-to-head.

## 3. Pacing: measured from 35 transcripts (25 hits, 10 flops)
Source: `raw/transcript_stats.json`, built by `tools/transcript_stats.py` from auto-captions.
"Hits" are 44-250x their channel median; "flops" are under 0.05x.

| Metric | Hits (median) | Flops (median) |
|---|---|---|
| Spoken rate | **174 wpm** | 212 wpm |
| Pauses > 0.7 s per minute | **15.5** | 10.2 |
| "you / your" per 1k words | **20** | 6.5 |
| "I / my / me" per 1k words | **37** | 4 |
| Runtime | 14.6 min | 12 min |

Caveat: 7 of the 10 flops are one channel (Wilytics), so channel style is mixed in. The three
non-Wilytics flops point the same way on rate (216 and 245 wpm, one at 165).

- **Spoken rate: about 175 wpm,** not rushed. The flops rattle along at more than 205 wpm with
  few pauses. 12-14 minutes is about **2,100-2,450 words**.
- **The narrator is a character.** Hits say "I" and "you" roughly 5x more often: "I downloaded
  every…", "you see that dot?" The linter now checks this (want "you" ≥10 and "I/my/me" ≥15 per
  1k words).
- **Pauses are content.** About 15 per minute: after a number, before a reveal, after a joke.

**How the hits open (first 45 s):**
1. **Show, don't announce.** Astroid (250x): "check it out, you see that all the way down there?
   That is 800 Pokémon, all properly scaled…" The thumbnail's image arrives in second 1.
2. **Fire surprising facts.** Newbie Indie Game Dev (162x): "Did you know half of the top 50 games
   on Steam are indie? … The word *life* appears in more titles than *death*…" Three fun facts in
   about 15 s, numbers within 2 s.
3. **Name the popular answer, then reframe it.** BlitzTalk (98x): "Everyone says the Browns and
   the Jets… my problem with those lists: they measure misery. That's not luck, that's being bad.
   I wanted to know which team the universe actually picked on." (This is a single, well-placed
   "not X, it's Y". It's fine once, at the reframe.)
4. **A second voice asks the viewer's question.** Data Time (120x, 105x) and Astroid use a skeptic
   or friend voice: "what's the longest word MrBeast ever said?" "Oh, he did a whole video on that."
   With TTS we can do this with a second, distinct voice. It's cheap, human-feeling, and breaks the
   monologue.
5. **A mystery with one strange data point.** Water CS2 (44x): "one single green dot… in North Korea."

Even the hits sometimes use clichés ("today we're diving into the data", "in this video we're
going to dive deep"). Clichés don't sink a strong idea, but they are free to remove, and for a
synthetic voice they are the first thing that sounds machine-made.
- **Visual change every 3-6 s.** There is no source for this exact number; it's the norm in the
  motion-graphics essay style. Change scale, highlight, camera, or a new element. Never hold a
  static chart longer than about 6 s.
- **Chain of loops.** Each 60-90 s segment raises a question, resolves it, and the resolution opens
  the next question. Use "but / therefore" connections between beats, never "and then".
- **Breathe after big reveals** (hits pause ~15x per minute). 0.5-1.0 s of silence after a key number, with the visual landing on
  the beat. The renderer inserts these from `[pause]` marks in the script.
- **The first 30 s are the main drop-off point** (YouTube's Key Moments report labels them
  "Intro"). The claim and the visual from the thumbnail must appear by 0:10.

## 4. Voice delivery (whichever voice the other agent picks)
- Generate per paragraph, not the whole script at once, so we can re-roll bad takes and keep tone consistent.
- Use SSML or the provider's style controls: slight emphasis on the key number, a pause before reveals.
- Pronunciation dictionary for game names, studio names and stats terms (e.g. "Baldur's Gate", "Hollow Knight", "roguelite").
- Keep **one voice, one persona** across the channel. A consistent narrator is a brand; random voices read as a content farm.
- Disclosure: YouTube requires labelling *realistic altered or synthetic* scenes. A synthetic
  narrator over original charts doesn't need it, but we'll tick the box if the voice imitates a
  real person.

## 5. Visuals: what reads as AI slop
- AI-generated "cinematic" images with a slow Ken Burns zoom.
- Generic stock footage that only roughly matches the line being spoken.
- Mixed visual styles (photo, then cartoon, then stock) with no art direction.
- Default fonts, default chart styles, the same transition on every cut.
- Every scene the same length; animations that start and end on the same beat every time.

## 6. Visuals: our look (fully generatable, consistent, ours)
1. **The chart is the protagonist.** Charts are built from our data, animated in Remotion, in one
   design system: a fixed palette, two fonts, and a fixed way of highlighting "the one dot".
2. **Real game assets as evidence, not decoration.** Steam header and capsule art, store
   screenshots, review-count counters, real review quotes in a "review card" component. They are
   used to show the thing being discussed, with commentary (standard fair-use practice for
   criticism and analysis; no full gameplay sequences or trailers).
3. **Hand-made touches.** Hand-drawn-style arrows and circles, annotations that appear as if
   written, an occasional "mistake" the narrator corrects ("wait, that's the wrong axis").
4. **Motion with intent.** Every move points at what the narration says (zoom to the dot as it's
   named, bars grow as the number is said). Timing comes from the voice's word timestamps.
5. **Recurring visual motifs.** A signature transition, a "model card" showing the score
   breakdown, and a running leaderboard. Recurring formats build recognition.
6. **No AI-generated images** of games, people or scenes. They are a strong slop signal and
   misrepresent real games.

## 7. Per-video quality gate (automated where possible)
- [ ] `script_lint.py` PASS (zero hard hits, soft penalty ≤ 5)
- [ ] Every claim traceable to our data or a named source (keep a `sources.md` per video)
- [ ] At least one genuine surprise the narrator reacts to
- [ ] The structure differs from the previous 3 uploads in at least one major way
- [ ] No static frame longer than 6 s (the renderer checks scene durations)
- [ ] Thumbnail promise paid off before the end; payoff placement noted
- [ ] A human watches the final cut once at 1.5x before publishing
