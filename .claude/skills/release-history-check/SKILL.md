---
name: release-history-check
description: Verify whether a candidate game launched on Steam first (or same day) or was released earlier elsewhere (Flash/browser, mobile, consoles, Japan/doujin, older PC, casual portals, inside another game), and record the verdict with a source. Use for every finalist and for comparison-group members before claiming anything about them.
---

# Release-history check (the Steam-first rule)

Why: a game that was already played somewhere else isn't "overlooked". In ep001, 34 of 51 top candidates failed this
check: Flash games, mobile ports, Japanese releases from years earlier, Big Fish casual games, XBLIG games, 1990s
re-releases. The model can't see any of that.

## Verdicts (`episodes/<ep>/release_history.json`, keyed by appid)
```json
"349760": ["PRIOR", "Snail Bob 2: free Flash game 2011 (bontegames.com/2011/06)"],
"251490": ["STEAM-FIRST", "Gravity Ghost: first released 2015-01-26 on PC (wikipedia Gravity_Ghost)"]
```
- `STEAM-FIRST`: Steam was first, or launched the same day as GOG, Humble or the developer's own site.
- `PRIOR`: released anywhere before its Steam date, including demos sold as full games, browser versions, mobile,
  console, regional releases, or as a mode inside another game.
- `DELISTED`: no longer sold on Steam.
- Every verdict carries a source: Wikipedia, press, the developer's site, SteamDB, MobyGames, DekuDeals and so on.

Plain re-releases of old games (1990s PC, Humongous, MicroProse "Classic") go in `exclusions.json` with a reason.
`finalists.py` reads both files: `PRIOR`/`DELISTED` become exclusion statuses, and unchecked games are marked
"unverified release history" and can't be finalists.

## How
- Batch the candidates to a few general-purpose agents (about 10 games each), with web search allowed. Ask for the
  earliest release anywhere, the platform, a source URL and a confidence level. Spot-check a sample yourself; the agent
  previously mislabelled one delisted game as PRIOR.
- Red flags worth checking first:
  - sequels whose earlier entry was PRIOR (Chicken Invaders, Lost Lands);
  - casual hidden-object publishers (Artifex Mundi, Big Fish, FIVE-BN);
  - Japanese doujin shooters;
  - "Classic", "HD", "Remastered" or "EX" in the name;
  - store dates before 2014;
  - Jackbox or console party games.
- After updating, re-run `finalists.py episodes/<ep>/exclusions.json`, `robustness.py`, facts and data, then confirm
  whether the final list changed.
- In the video and fine print, say how many were checked and how many groups still contain unchecked games.
