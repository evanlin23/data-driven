# Copyright & Policy Risk — Data-Story Game Channel

Researched 2026-11-05. US creator, YPP-targeted, daily automated uploads, TTS narrator, Remotion charts + game assets.
Not legal advice. Policies below change; re-check the primary pages quarterly.

**Source tags:** **[P]** = verified-primary (fetched the official page this session). **[P-recall]** = primary source cited from known law/text, not re-fetched. **[S]** = secondary (press/blog/forum). Unverified SEO-blog claims are flagged as such.

---

## 1. Game assets

### 1.1 Legal baseline (US fair use, 17 U.S.C. §107)
- Four factors: purpose/character, nature of work, amount used, market effect. Only a court decides fair use. YouTube itself says so: "only a court can decide" [P, YouTube "Common copyright myths", support.google.com/youtube/answer/2797449].
- *Campbell v. Acuff-Rose* (1994): commercial use does not defeat fair use; transformativeness is central [P-recall].
- *Andy Warhol Found. v. Goldsmith* (2023): "transformative" now means a *different purpose*, judged use by use. Using a game's key art as a **decorative/commercial thumbnail** serves the same purpose as the original promo art, which is weak. Showing a screenshot **as the subject of analysis** ("this is the store page the model flagged") is a different purpose, which is stronger [P-recall].
- *Kelly v. Arriba* / *Perfect 10 v. Amazon* (9th Cir.): small reference images used for identification or indexing were fair use. This supports small capsule images as data labels in charts [P-recall].
- *Feist v. Rural* (1991): facts such as prices, review counts, playtimes and release dates are not copyrightable. Your charts of Steam numbers are your own expression [P-recall]. Contract/ToS limits on *how you got* the data are a separate question (see §3).
- **Practical reality:** fair use is a defense you argue *after* a claim. Content ID does not evaluate it. The real risk is automated matching, not lawsuits.

### 1.2 What triggers Content ID / manual claims (ranked)
1. **Game soundtrack / licensed music, including trailer audio.** This is by far the most common trigger. Labels and distributors (and some publishers' music arms) register OSTs in Content ID. Trailer audio often contains licensed songs that are claimed even when the publisher would not object. Ubisoft says it outright: monetization is permitted "unless the video includes copyrighted music" flagged by Content ID, and don't dispute music claims without a direct license [P, ubisoft.com/en-us/videopolicy.html, updated Jan 2016]. EA: third-party licensors "may object to your use of their music" [S, EA content-policy page via search snippet; the primary page returned 503].
2. **Official trailers used verbatim or in long stretches.** Publishers and their MCN/agency partners sometimes register trailers. Ubisoft: "Simply duplicating official trailers, TV ads... is not authorized and will likely result in removal" [P].
3. **Long uninterrupted gameplay with game audio.** Cutscene and score audio matches.
4. **Capsule/header art, screenshots, logos.** Content ID rarely matches stills in long-form video. The risk is a **manual claim/takedown** (rare for analysis channels) or **trademark/false-endorsement** confusion if logos dominate a thumbnail.

What a claim means [P, support.google.com/youtube/answer/6013276]: claims hit the video, not the channel, and are **not strikes**. Owners can block, track, or monetize. On videos over 3 minutes, music claims usually just divert revenue. You can mute or erase the song, trim it, or swap in Audio Library audio to release the claim. A dispute without a valid basis can lead to a takedown, and a takedown is a **strike** (3 strikes = termination). **Never auto-dispute.**

### 1.3 Publisher video policies

| Publisher | Monetized YPP use? | Key restrictions | Status |
|---|---|---|---|
| **Valve** (Valve-owned games only) | Yes: "via the YouTube partner program and similar programs" | No paywall/sale/licensing of videos; don't distribute assets (music, voice) separately; third-party content (e.g., music) needs owner permission; policy "applies only to Valve content" and does **not** cover third-party Steam games | [P] store.steampowered.com/video_policy |
| **Nintendo** | Yes, YPP is a listed program | Must add "creative input or commentary"; no bare uploads of trailers/music/art; only released content (or official promo material); no datamined assets; individuals only (corporate entities not covered); no implied affiliation; thumbnails not addressed | [P] nintendo.co.jp/networkservice_guideline/en/ |
| **Microsoft / Xbox Game Studios** | Yes: ad revenue on YouTube/Twitch | Required notice: game © Microsoft, made under Game Content Usage Rules, not endorsed by Microsoft, plus a link to the Rules; don't use Microsoft game **logos** as your logo; soundtracks often third-party licensed (Halo 3 music is the only explicit grant); no subscription-gating; rules dated Jan 2015; Minecraft has separate rules | [P] xbox.com/en-US/developers/rules |
| **Ubisoft** | Yes, YPP and similar | No Content-ID-flagged music; no verbatim trailers/TV ads; pre-release footage may be blocked; no paid access; updated Jan 2016 | [P] ubisoft.com/en-us/videopolicy.html |
| **Capcom** | Yes: partner programs/ads on YouTube, Twitch, Facebook | No standalone soundtrack/BGM/SFX; no standalone cutscenes; no pre-release/leaked footage; official logos/art not allowed as Twitch emotes; updated Mar 15 2021 | [P] capcomusa.com/video-policy/ |
| **EA** | Yes: "monetization of videos via partner programs (like YouTube or Twitch)" | Third-party music may be claimed; released versions only (2013-16 staff statements) | [S] help.ea.com content-policy (page 503'd at fetch; quoted via search) |
| **Sony / PlayStation Studios** | **No public written policy found** | Common practice is permissive and in-game licensed music is claimed, but this is forum/anecdotal only | [S], unverified. Treat as "fair use only" |
| **Indie / third-party Steam games** | Covered by no blanket policy | Most indies welcome coverage, but there's no written license; Valve's policy does not extend to them | Treat as fair use |

**Conflict to note:** SEO blogs (e.g., vidIQ) state "PlayStation allows monetization of exclusives." No Sony primary source backs this. Don't rely on it.

**Thumbnails:** none of the policies above addresses thumbnails explicitly. Fair-use analysis for thumbnails is weaker (post-*Warhol*: decorative or promotional purpose). Mitigation: put the **chart, number, or your own graphic as the hero**. Game art should be one element (cropped or framed, small, with a data overlay). Use no publisher logos and no official key art as a full-bleed background.

---

## 2. Quoting Steam user reviews

- **Copyright:** review authors keep copyright. Under the Steam Subscriber Agreement §6.A, users grant **Valve** (not you) a license [P, store.steampowered.com/subscriber_agreement]. Short quotes (1-2 sentences) used *as evidence in an analysis* are a strong fair use (small amount, commentary purpose, no market substitute). Don't stack dozens of full reviews on screen.
- **Privacy / harassment:** usernames are public, but showing them adds little analytical value and invites brigading of individuals. YouTube's harassment policy applies if a video singles out a private person for ridicule [S/P-recall].
- **Rule:** quote short excerpts, **anonymize** ("Steam reviewer, 340 hrs played"), don't show avatars, and don't mock individuals. Correct obvious typos only with [sic] or not at all. Never fabricate or paraphrase a review and present it as a quote.

---

## 3. Data terms

| Source | What the terms say | Monetized video / companion site? | Status |
|---|---|---|---|
| **Steam Web API** (key-based) | 100,000 calls/day; must "implement the Valve name(s), logo(s), and links to Valve"; links must not be nofollowed; no implication of endorsement or affiliation; must have a privacy policy if handling user data; Valve may terminate any time; WA law | No general commercial-use bar. The license is framed around distributing "Steam Data" to end users. Charts of aggregate public stats in videos are low risk. On the site, add "Data from Steam. Not affiliated with Valve." and a followed link | [P] steamcommunity.com/dev/apiterms |
| **Store endpoints** (`store.steampowered.com/api/appdetails`, `/appreviews/`) | Not part of the documented Web API, so no published terms beyond the Subscriber Agreement. SSA limits Content to "personal, non-commercial use" (§2.A), bars copying/publishing Content without consent (§2.G), and bars "scripts, bots" (§4.C, context is account/service use) | **Grey zone.** Facts (counts, prices, scores) are not copyrightable (*Feist*), and this access is universal in the industry. Risk = rate-limit/IP block, not lawsuits. Don't republish review *text* in bulk on the site; publish derived aggregates only. Throttle requests (~1 req/1.5 s is common practice [S]) | [P] SSA; endpoint terms absent |
| **SteamSpy** | No ToS, license, or attribution clause on /about; footer "Copyright © 2015-2021 Sergey Galyonkin"; data is *extrapolated* and "isn't 100% correct" | No explicit permission or prohibition. Credit "SteamSpy" on screen and on the site as courtesy and accuracy disclosure. Label owner counts as **estimates/ranges** | [P] steamspy.com/about |
| **IGDB** (Twitch) | Primary docs blocked (403). Secondary sources conflict: an older Twitch staff post says commercial use is "fine"; newer aggregators say free for non-commercial use, commercial use needs a partnership, attribution expected; 4 req/s | **Unresolved.** Before monetized use, read api-docs.igdb.com and the Twitch Developer Services Agreement, or email Twitch for written OK. Always credit "IGDB.com" | [S], conflict |
| **OpenCritic** | API is a paid RapidAPI product; founder publicly pushed for licensing or credit | Use the paid API under its plan terms, or skip it. Don't scrape | [S] |
| **HowLongToBeat** | ToS could not be fetched (site blocks bots); no public API | **Highest data risk.** Scraping a site with no API and anti-bot measures is a ToS problem. Either skip it, use a few manually checked numbers with credit, or ask permission | Unverified |

Attribution standard for the pipeline: end-card plus description line: "Data: Steam (Valve), SteamSpy estimates, [others]. Not affiliated with or endorsed by Valve or any publisher." The companion site needs a matching footer with a followed link to store.steampowered.com.

---

## 4. YouTube monetization policy

**Inauthentic content** (renamed from "repetitious content", update dated **July 15, 2025**) [P, support.google.com/youtube/answer/1311392]:
- Content must "not be mass-produced, generic, repetitive, or manipulative"; flagged if it "looks like it's made with a template."
- Explicitly not allowed: "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"; "AI-generated content made with generic or unoriginal templates giving the impression of mass production."
- Allowed: automated tools/templates **if** "the final product must still demonstrate your creative vision."
- **Reused content** is unchanged: no "minimal changes" to others' content. A video built mostly from trailers plus TTS is the textbook reused-content rejection.

**Fit for this format:** a real model, original analysis and original charts is the *right* side of the line. The danger is **sameness across a daily catalog**: identical structure, intro, chart sequence, phrasing ("In this video we'll..."), and thumbnail template. Reviewers judge the channel as a whole [P, answer/72851]. Commonly cited review focus areas are the main theme, most-viewed, newest, highest-watch-time videos, and metadata [S/P-recall, YPP review FAQ, not re-fetched]. Vary the narrative arc, chart types, hooks, and length per topic. Make each video answer a distinct question with a distinct finding.

**Gaming-specific** [P, answer/138161]: monetization depends on publisher-granted rights. Long stretches of gameplay "for extended periods of time" may be rejected. Commentary must be "strictly tied to the live action being shown." So **footage must illustrate the narration, never fill time.**

**AI disclosure ("altered or synthetic content")** [P, answer/14328491]: disclosure is required for *realistic* content: a real person saying or doing something they didn't, altered real events or places, realistic fake scenes, or AI music as the main focus. Not required for productivity uses (scripts, captions, infographics), non-realistic content, or cloning **your own** voice for voiceover. The page does **not** mention generic TTS narrators. Reading: a synthetic narrator that isn't impersonating a real person is **not required** to be labeled. **Do not** clone or imitate a real person's voice (a streamer, a celebrity narrator); that triggers disclosure and likely likeness/impersonation issues. Blogs claiming "all AI voices need the label" or "the label hurts reach" are unverified [S]. Optionally add a description line ("Narration voiced with TTS") for transparency.

**Daily automated uploads:** YouTube sets no frequency limit, but volume plus template sameness is exactly the "mass-produced" signal. Have a human review each script and video before publishing. Avoid uploading via the API with no human in the loop until YPP is approved and the format is established.

---

## 5. Music

- **Safest:** YouTube Audio Library. YouTube says Audio Library tracks "are not claimed... through Content ID" and are monetizable in YPP. CC-BY tracks need artist credit in the description. YouTube warns that only Audio Library content is "known to YouTube to be copyright-safe" and it is not responsible for third-party "royalty-free" music [P, answer/3376882]. Audio Library licensing for use *off* YouTube (e.g., the companion site) is not stated, so don't reuse it there.
- **Next safest:** a subscription library with a channel-whitelisting system (Epidemic Sound, Artlist, Musicbed, etc.). Whitelist the channel ID **before** first upload, and keep the license active, since tracks used after cancellation can be claimed [S, vendor terms vary; verify the plan covers monetized YouTube].
- **Pitfalls:** "royalty-free" or "no copyright" tracks from random YouTube channels or SoundCloud are often later registered in Content ID by distributors (the most common bogus-claim source) [S]. **Never** use game OSTs, trailer audio, or AI-music services whose terms don't grant monetized YouTube use and Content ID safety. Mute game audio on all B-roll by default.

---

## 6. Pipeline rules

### DO
1. Build every video around an original finding: script → chart → footage illustrates the claim, not the reverse.
2. Use **Audio Library or whitelisted-licensed** music only. Log track ID and license per video.
3. **Mute game audio** on all gameplay/trailer B-roll. Keep clips ≤ ~5-8 s each and ≤ ~20-25% of runtime overall (internal heuristic, not a legal threshold).
4. Prefer **own-captured gameplay** (Steam recording / OBS of released builds) over publisher trailers.
5. Use capsule/header art at small size as *data labels* in charts; screenshots only when the narration discusses them.
6. Make the thumbnail hero your chart/number/graphic; game art is cropped and secondary.
7. Anonymize review quotes ("Steam reviewer, N hrs"); keep excerpts to ≤ 2 sentences.
8. Add a description boilerplate: data credits (Steam/Valve, SteamSpy estimates, IGDB if used), "Not affiliated with Valve or any publisher," the Microsoft notice + link whenever an Xbox Game Studios title appears, and CC-BY music credits.
9. Have a human approve each upload. Vary structure, hook, chart types and length across the catalog.
10. Re-check the in-Studio copyright pre-check ("Checks") before publishing and fix any match by trimming or muting.

### DON'T
1. Don't use game soundtracks, trailer audio, or licensed songs, even "just 10 seconds."
2. Don't play trailers verbatim or show long uninterrupted gameplay.
3. Don't use publisher/game **logos** as thumbnail focal points, and don't imply endorsement ("Official", Steam logo branding).
4. Don't show pre-release, leaked, datamined, or embargoed content.
5. Don't auto-dispute claims. Dispute only with a license or a clear fair-use case, reviewed by a human.
6. Don't show reviewer usernames/avatars or target individuals.
7. Don't scrape HowLongToBeat/OpenCritic, or use IGDB commercially, without confirmed terms.
8. Don't clone or imitate a real person's voice.
9. Don't bulk-republish Steam review text on the companion site.
10. Don't present SteamSpy owner estimates as exact figures.

### Risk table

| Asset / practice | Risk | Mitigation |
|---|---|---|
| Game OST / BGM | **High** (Content ID claim; revenue lost or video blocked) | Never use; mute |
| Trailer audio (licensed songs) | **High** | Mute; use own audio bed |
| Trailer video, verbatim/long | **Med-High** (claim/removal; reused-content flag) | Short muted cuts or own capture |
| Gameplay footage, muted, short, narrated | **Low** (Med for Sony, which has no written policy) | Tie to narration; cap runtime share |
| Store screenshots in body | **Low** | Show as analysis subject; small, with overlays |
| Capsule/header art as chart labels | **Low** | Small, many at once (indexing use) |
| Capsule/key art as thumbnail hero | **Medium** | Chart-led thumbnail; crop/frame art |
| Publisher/game logos | **Medium** (trademark/endorsement) | Omit or keep tiny; no "official" framing |
| Steam review quotes w/ usernames | **Medium** (privacy/harassment) | Anonymize; short excerpts |
| Steam Web API data | **Low** | Attribution + link; ≤100k calls/day |
| Store `appdetails`/`appreviews` | **Low-Med** (ToS grey, IP blocks) | Throttle; publish aggregates only |
| SteamSpy data | **Low** | Credit; label as estimates |
| IGDB data | **Medium** (commercial terms unclear) | Get written OK or skip |
| HowLongToBeat scraping | **Med-High** (ToS, blocking) | Skip, manual-cite, or ask |
| OpenCritic | **Medium** | Paid API or skip |
| Generic TTS narrator | **Low** (no label required) | Don't impersonate real voices |
| Daily templated uploads | **High for YPP approval** (inauthentic content) | Human review; vary format; original findings |
| Audio Library music | **Very low** | Credit CC-BY tracks |
| "Royalty-free" music from random sources | **Medium-High** | Avoid |

---

### Sources
- YouTube monetization policies (inauthentic/reused): https://support.google.com/youtube/answer/1311392 [P]
- YouTube altered/synthetic disclosure: https://support.google.com/youtube/answer/14328491 [P]
- YouTube copyright claims: https://support.google.com/youtube/answer/6013276 [P]
- YouTube copyright myths / fair use: https://support.google.com/youtube/answer/2797449 [P]
- YouTube video game content monetization: https://support.google.com/youtube/answer/138161 [P]
- YPP overview/eligibility: https://support.google.com/youtube/answer/72851 [P]
- YouTube Audio Library: https://support.google.com/youtube/answer/3376882 [P]
- Valve video policy: https://store.steampowered.com/video_policy [P]
- Steam Web API Terms: https://steamcommunity.com/dev/apiterms [P]
- Steam Subscriber Agreement: https://store.steampowered.com/subscriber_agreement/ [P]
- SteamSpy about: https://steamspy.com/about [P]
- Nintendo Game Content Guidelines: https://www.nintendo.co.jp/networkservice_guideline/en/index.html [P]
- Microsoft Game Content Usage Rules: https://www.xbox.com/en-US/developers/rules [P]
- Ubisoft video policy: https://www.ubisoft.com/en-us/videopolicy.html [P]
- Capcom video policy: https://www.capcomusa.com/video-policy/ [P]
- EA content policy: https://help.ea.com/en/articles/security-and-rules/ea-content-policy/ [S, 503 at fetch]
- IGDB commercial-use thread: https://discuss.dev.twitch.com/t/commercial-use-of-igdb-api/23567 [S]
- OpenCritic API listing: https://rapidapi.com/opencritic-opencritic-default/api/opencritic-api [S]
- Case law: Campbell v. Acuff-Rose (1994); Andy Warhol Found. v. Goldsmith (2023); Kelly v. Arriba Soft (9th Cir. 2003); Perfect 10 v. Amazon (9th Cir. 2007); Feist v. Rural (1991) [P-recall]
