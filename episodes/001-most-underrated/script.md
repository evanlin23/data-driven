# Episode 001: I Built a Model to Find the Most Underrated Game on Steam (v4: KNN model, Steam-first verified, consensus order)
# Every number comes from facts.json (pipeline/ep001_facts.py) or robustness.json. Rounded only for speech. '|' = line break.

@chapter The red dot
@scene scatter @ref:scatter_hero {"highlightAt": 2.0}
See that red dot? That's a game. Ninety-six percent of its players liked it.
It costs ten dollars... and it has three hundred and two reviews. [pause 0.5]
Games like it usually ended up with about two thousand.

@scene textBeat {"text": "Same launch day as one of|the *biggest* games of 2015.", "size": 84}
Oh, and it launched on the exact same day as one of the biggest games of that year. Hold that thought.

@scene textBeat {"text": "51,897 games. One question.", "sub": "Given how good it is, how many people should have played it?"}
I wanted to find the games this happened to the worst. I scored fifty-one thousand, eight hundred and ninety-seven Steam games, all with one question. [pause 0.4]
Given how good a game is, how many people should have played it? And which games got robbed the hardest?
That red dot is on my list. You'll see where at the end.

@chapter How the model works
@scene scatter @ref:scatter_cloud
Here's a sample of those games. Left to right is how much players liked it. Bottom to top is how many reviews it has.

@scene bigNumber {"value": 130, "kind": "int", "label": "owners for every review", "sub": "typical for the games in this video (SteamSpy estimates)", "color": "gold"}
Steam doesn't publish sales, so I'm using reviews instead. For the games on my list, there's roughly one review for every hundred and thirty owners.
Reviews aren't players, and that ratio moves around a lot. But more reviews generally means more players, so it's the best yardstick I've got.

@scene textBeat {"text": "20 out of 20 is *not* better|than 9,800 out of 10,000."}
Now, ratings. You can't just sort by percent positive.
A game with twenty reviews, all positive, isn't better than a game with nine thousand eight hundred out of ten thousand.
So I pull every score toward the Steam average, which is eighty percent. The fewer reviews a game has, the harder it gets pulled.

@scene textBeat {"text": "150 games just like it:|same rating, same launch window.", "size": 80}
Here's the model. For every game, I find the hundred and fifty games most like it. Released around the same time, with almost the same rating.
Whatever the typical one of those got, that's what I call expected.

@scene scatter @ref:scatter_trend
That gold line is what games from early 2015 usually got, at every rating. Better games get more reviews. You'd hope so.

@scene textBeat {"text": "expects 1,000 · has 100|= *10x* short"}
Here's the number I rank by. Say a game's lookalikes usually got a thousand reviews, and it only has a hundred.
That's ten times short. The bigger that number, the harder a game got robbed.

@scene bigNumber {"value": 2.7, "kind": "x1", "label": "how far off the model is on a typical game", "sub": "so a game only counts as robbed when it's well past that", "color": "text"}
Is this perfect? No. On a typical game, the prediction is off by about two point seven times, one way or the other.
So a game only counts as robbed when it's well past that.

@chapter The rules
@scene textBeat {"text": "The rules", "sub": "released 2014 or later · 200+ reviews · no DLC · one game per studio"}
A few rules. Only games released from 2014 on, because Steam reviews didn't exist until late 2013. At least two hundred reviews, so a handful of fans can't fake it.
No DLC. And one game per studio, so no single developer hogs the list.

@scene bigNumber {"value": 34, "kind": "int", "label": "of the 51 games I checked had been released somewhere else first", "sub": "browser and Flash games, mobile, older PC versions, Japan", "color": "accent"}
And one more rule, which ended up mattering more than anything else. The game has to have launched on Steam first.
I checked fifty-one of the top candidates by hand. Thirty-four of them had already been out somewhere else. Free Flash games, phone games, games that came out years earlier in Japan.
Those aren't overlooked. Their fans just played them somewhere else first. So they're out.

@scene textBeat {"text": "7 versions of the model.|Same *top seven* every time.", "size": 84}
Last thing. I ran the model seven different ways. The same seven games made the top ten every single time. The final order is the average.

@chapter #10 to #6
@scene leaderboard @ref:board_10
Numbers ten to six are closer calls, about three times short, which isn't far past the model's normal error. Call them probably overlooked.

@scene gapBars @ref:gap_399600
Number ten. I and Me. Ninety-six percent positive. Games like it usually got about nine hundred reviews. It has three hundred and fifty-eight.

@scene gapBars @ref:gap_377690
Number nine. Starlight Vega, a visual novel. Ninety-three percent positive, and about two point eight times short.

@scene gapBars @ref:gap_236930
Number eight. Blackwell Epiphany, the final game in Wadjet Eye's Blackwell series.
Ninety-eight percent positive. That's the highest rating in the whole top ten.

@scene gapBars @ref:gap_389650
Number seven. Stardust Galaxy Warriors, a couch co-op space shooter. Two hundred and twenty-six reviews, against about seven hundred expected.

@scene gameCard @ref:card_317320
Number six. Nelly Cootalot: The Fowl Fleet. A pirate point-and-click adventure, and its store page says Tom Baker is in the cast.
Eighty-one on Metacritic, the best critic score on the list. Three point two times short.

@chapter Was it bad timing?
@scene textBeat {"text": "So it's bad *timing*.|Right?", "size": 96}
Before the top five, I want to test a theory. Remember that red dot launching next to a giant? Maybe that's the whole story. Good games, buried by bad timing.

@scene bigNumber {"value": 0.74, "kind": "pct", "label": "of random Steam games launched within a week of a mega-hit", "sub": "mega-hit = one of Steam's 400 most-reviewed games · sample of 141 established games", "color": "text"}
So I took Steam's four hundred most-reviewed games, and checked launch dates against them.
Almost three in four random Steam games launched within a week of one of those hits. There's always a giant nearby.

@scene bigNumber {"value": 0.63, "kind": "pct", "label": "of the most underrated-looking games did", "sub": "95 games with known launch dates", "color": "accent"}
The most underrated-looking games? A bit under two in three. If anything, slightly fewer.
Bad timing makes a good story. But it isn't the pattern.

@chapter What they have in common
@scene compareBars {"title": "What kind of games get overlooked?", "aLabel": "100 most underrated-looking", "bLabel": "random Steam games", "rows": [{"label": "Casual", "a": 0.48, "b": 0.225}, {"label": "Strategy", "a": 0.11, "b": 0.306}, {"label": "Simulation", "a": 0.08, "b": 0.312}, {"label": "RPG", "a": 0.12, "b": 0.294}], "note": "Steam store genres · 100 top-rated games furthest below expectations vs a random sample of 160 established games"}
So what do they have in common? Genre, for one. Casual games show up about twice as often on the underrated side.
Strategy and RPGs show up about a third as often, and simulation about a quarter. My guess? Those genres have fans who go digging for new games.

@scene compareBars {"title": "Who do you play it with?", "aLabel": "100 most underrated-looking", "bLabel": "random Steam games", "rows": [{"label": "Single-player", "a": 0.98, "b": 0.906}, {"label": "Multiplayer", "a": 0.20, "b": 0.362}, {"label": "Online PvP", "a": 0.03, "b": 0.212}], "note": "Steam store categories · same samples"}
Almost all of them are single-player. But so are most Steam games. The real gap is online PvP.
Three percent of the underrated-looking games have it. Twenty-one percent of random Steam games do.
My guess: multiplayer games spread because your friends drag you in. Nobody drags you into a puzzle game.

@scene bigNumber {"value": 0.02, "kind": "pct", "label": "of them cost $20 or more", "sub": "vs 17% of top-rated games that got the reviews they should have", "color": "accent"}
And they're rarely expensive. Only two percent cost twenty dollars or more. Among top-rated games that got the reviews they should have, it's seventeen percent.
I can't prove why from this data. My guess: cheap often means a tiny team with no marketing budget.

@chapter #5 to #2
@scene gameCard @ref:card_262850
The top five. Number five. The Journey Down, Chapter Two. A point-and-click adventure, and seventy-eight on Metacritic.

@scene gapBars @ref:gap_262850
Ninety-five percent positive. Games like it usually got about twenty-three hundred reviews. It has five hundred and thirty-seven. Four point three times short.

@scene gameCard @ref:card_422110
Number four. Wand Wars. According to its store page, you ride brooms, cast spells, and turn your enemies into chickens.

@scene gapBars @ref:gap_422110
Ninety-six percent positive. About eleven hundred reviews expected. It has two hundred and eighteen. Five point two times short.
And yes, it's multiplayer. But couch multiplayer: your friends have to be in the room. No online PvP.

@scene gameCard @ref:card_415920
Number three. Voidspire Tactics, a turn-based tactics RPG where you build your own party.

@scene gapBars @ref:gap_415920
Ninety-six percent positive. About fourteen hundred expected. Two hundred and sixty-eight reviews. Five point three times short.

@scene launchCollision @ref:collision_415920 {"caption": "7 days later: Fallout 4"}
It came out November 2nd, 2015. One week later, Fallout 4 launched. Bad luck? Sure. But remember, not the pattern.

@scene gameCard @ref:card_255340
Number two. Escape Goat 2. A puzzle platformer where you team up with a friendly mouse to get out of a dungeon.

@scene gapBars @ref:gap_255340
Ninety-five percent positive. Almost twenty-nine hundred reviews expected. It has four hundred and forty-one. Six point five times short.
And honestly? Number one and number two are neck and neck. In three of my seven versions of the model, this was number one.

@chapter #1
@scene scatter @ref:scatter_hero_trend
But in the other four, it was this. Remember the red dot? Ninety-six percent liked it. Three hundred and two reviews.
Games like it usually got about two thousand. That's six point six times short.

@scene gameCard @ref:card_251490
It's Gravity Ghost, by Ivy Games. You run, jump, and glide around tiny planets, using gravity to rescue survivors across a shattered galaxy.
Players gave it ninety-six percent. Critics gave it a seventy-five.

@scene launchCollision @ref:collision_251490 {"caption": "Same day: Dying Light"}
And here's the launch day I told you to hold onto. January 26th, 2015. [pause 0.5]
The same day as Dying Light. Dying Light has four hundred and fifty-seven thousand reviews. Gravity Ghost has three hundred and two.

@scene lineChart @ref:hero_history
I know, I just told you timing isn't the pattern. But for this one, that week? It can't have helped.
This is its whole life on Steam, month by month. A small bump at launch, then a trickle that never quite stopped.
Should have: about two thousand reviews. Got: three hundred and two.

@chapter What did the model miss?
@scene textBeat {"text": "Which game did my model *miss*?", "sub": "Next: the most OVERRATED game on Steam"}
That's the list. Your favourite hidden gem probably isn't on it. Tell me which game my model missed.
Next time I'm flipping the model around: the most overrated game on Steam. That one's going to start some fights.
