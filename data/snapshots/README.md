# Raw data snapshots

`raw-2026-11-05.tgz`: everything under `data/raw/` as fetched on 2026-11-05 (6.7 MB compressed):
SteamSpy catalogue (87 pages, ~87k apps), SteamSpy details sample, Steam store details (finalists, 400 most-reviewed
games, 160-game random sample), monthly review histograms.

Restore instead of re-fetching (SteamSpy's rate limit makes a full fetch take ~1.5 h):

    tar -xzf data/snapshots/raw-2026-11-05.tgz -C data
