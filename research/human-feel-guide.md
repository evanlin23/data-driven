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
- Planned: transcripts of the 25 top and 10 bottom videos (`transcript_video_ids.txt`), to measure
  the real pacing of hits. Pending, because YouTube bot-walls this container; the transcripts must
  be fetched from a normal machine.

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

## 3. Pacing
- **Spoken rate.** Industry guidance for explainer narration is 130-160 wpm; one sample of 53
  long-form voiceovers had a median of about 166 wpm. Target **150-165 wpm**, so 11-13 minutes is
  about **1,700-2,100 words**. We'll calibrate against the top-video transcripts once we have them.
- **Visual change every 3-6 s.** There is no source for this exact number; it's the norm in the
  motion-graphics essay style. Change scale, highlight, camera, or a new element. Never hold a
  static chart longer than about 6 s.
- **Chain of loops.** Each 60-90 s segment raises a question, resolves it, and the resolution opens
  the next question. Use "but / therefore" connections between beats, never "and then".
- **Breathe after big reveals.** 0.5-1.0 s of silence after a key number, with the visual landing on
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
