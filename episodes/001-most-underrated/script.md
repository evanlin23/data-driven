# Episode 001: I Built a Model to Find the Most Underrated Game on Steam (v3, after full QA)
# Every number comes from facts.json (pipeline/ep001_facts.py). Rounded only for speech. '|' in textBeat = line break.

@chapter The red dot
@scene scatter @ref:scatter_hero {"highlightAt": 2.0}
See that red dot? That's a game. Ninety-seven percent of its players liked it.
It costs three dollars... and it has two hundred and eight reviews. [pause 0.5]
Games that well liked usually get thousands.

@scene textBeat {"text": "What is it?|*Not* what you'd guess.", "size": 96}
I'm not telling you what it is yet. But it's not the kind of game you'd guess.

@scene textBeat {"text": "51,897 games. One question.", "sub": "Given how good it is, how many people should have played it?"}
I wanted to know how often this happens. I scored fifty-one thousand, eight hundred and ninety-seven Steam games, all with one question. [pause 0.4]
Given how good a game is, how many people should have played it? And which games got robbed the hardest?
That red dot is on my list. You'll see where at the end.

@chapter How the model works
@scene scatter @ref:scatter_cloud
Here's a sample of those games. Left to right is how much players liked it. Bottom to top is how many reviews it has.

@scene bigNumber {"value": 0.02, "kind": "pct", "label": "of owners leave a review", "sub": "about 1 in 50 for the games in this video", "color": "gold"}
Steam doesn't publish sales, so I'm using reviews instead.
For the games on my list, SteamSpy's estimates work out to roughly one review for every fifty owners.
Reviews aren't players. But more reviews means more players, and that's all I need.

@scene textBeat {"text": "20 out of 20 is *not* better|than 9,800 out of 10,000."}
Now, ratings. You can't just sort by percent positive.
A game with twenty reviews, all positive, isn't better than a game with nine thousand eight hundred out of ten thousand.
So I pull every score toward the Steam average, which is eighty percent. The fewer reviews a game has, the harder it gets pulled.

@scene scatter @ref:scatter_trend
Better games get more reviews. You'd hope so. That gold line is my model. [pause 0.3]
Give it a game's rating and when it came out, and it tells you how many reviews a game like that usually ends up with.
I trained it on every game with at least ten reviews, so it knows what normal looks like, not just what hits look like.

@scene textBeat {"text": "model expects 1,000 reviews|game has 100|= *10x* short"}
Here's the number I rank by. Say the model expects a thousand reviews, and a game only has a hundred.
That's ten times short. The bigger that number, the harder a game got robbed.

@scene bigNumber {"value": 2.7, "kind": "x1", "label": "how far off the model is on a typical game", "sub": "so a game only counts as robbed when it's way past that", "color": "text"}
Is the model perfect? No. On a typical game, it's off by about two point seven times, one way or the other.
That's why a game only counts as robbed when it's way past that. Everything on my list is at least five times short.

@chapter The rules
@scene textBeat {"text": "The rules", "sub": "Released 2014 or later · no re-releases · no DLC · 200+ reviews · one game per studio"}
A few rules. Only games released from 2014 on, because Steam reviews didn't exist until late 2013.
No re-releases of older games, and no DLC.

@scene textBeat {"text": "200+ reviews.|One game per studio.", "size": 88}
To make the list, a game needs at least two hundred reviews, so a handful of fans can't fake it. About fifteen thousand games qualify.
And one game per studio, or a single developer would take three spots.

@scene textBeat {"text": "Top 3: rock solid.|4 to 10: *a close race*.", "size": 84}
One more thing. I tuned the model a few different ways. The top three never moved. Below that, it's a closer race, so treat the exact order loosely.

@chapter #10 to #6
@scene leaderboard @ref:board_10
These ten got robbed the worst. Let's count down.

@scene gameCard @ref:card_516480
Number ten. Pinkman. A platformer about a man with pink skin and, according to its own store page, an incredible skill to fart.
It costs ninety-nine cents. Ninety-eight percent positive. The model expected about thirty-seven hundred reviews. It has six hundred and sixty-seven.

@scene gameCard @ref:card_344860
Number nine. Crystal Story Two. A turn-based RPG about a young dragon trying to stop an evil witch.
Ninety-four percent positive, three dollars. The model expected around eighteen hundred reviews. It has three hundred and twenty-five.

@scene gameCard @ref:card_415920
Number eight. Voidspire Tactics, a tactics RPG with a party you build yourself.
Ninety-six percent positive. The model expected about eighteen hundred reviews. It has two hundred and sixty-eight.

@scene launchCollision @ref:collision_415920 {"caption": "7 days later: Fallout 4"}
It came out November 2nd, 2015. One week later, Fallout 4 launched.

@scene gameCard @ref:card_259810
Number seven. Home Sheep Home: Farmageddon Party Edition. Yes, it's a Shaun the Sheep game.
Ninety-six percent positive. The model expected over five thousand reviews. It has seven hundred and fifty-seven.

@scene gameCard @ref:card_412670
Number six. Bullet Heaven 2. A bullet-hell shooter where you dodge hundreds of bullets a second.
Ninety-eight percent positive. The model expected almost thirty-eight hundred reviews. It has four hundred and ninety-three.

@scene launchCollision @ref:collision_412670 {"caption": "6 days earlier: Rainbow Six Siege"}
It came out December 7th, 2015. Six days earlier, Rainbow Six Siege launched. Siege has over a million reviews today.

@chapter Was it bad timing?
@scene textBeat {"text": "So it's bad *timing*.|Right?", "size": 96}
At this point I had a theory. These games launched right next to giants, and got buried.
It's a great story. So I checked it.

@scene bigNumber {"value": 0.74, "kind": "pct", "label": "of random Steam games launched within a week of a mega-hit", "sub": "mega-hit = one of Steam's 400 most-reviewed games · sample of 141 games", "color": "text"}
I took Steam's four hundred most-reviewed games, and checked launch dates against them.
Almost three in four random Steam games launched within a week of one of those hits. There's always a giant nearby.

@scene bigNumber {"value": 0.65, "kind": "pct", "label": "of the 100 most underrated did", "color": "accent"}
The hundred most underrated? About two in three. If anything, slightly fewer.
Bad timing makes a good story. But it isn't the pattern.

@chapter What underrated games have in common
@scene compareBars {"title": "What kind of games get overlooked?", "aLabel": "100 most underrated", "bLabel": "random Steam games", "rows": [{"label": "Casual", "a": 0.35, "b": 0.225}, {"label": "Strategy", "a": 0.10, "b": 0.306}, {"label": "Simulation", "a": 0.06, "b": 0.312}, {"label": "RPG", "a": 0.11, "b": 0.294}], "note": "Steam store genres · 100 most-underrated games vs a random sample of 160"}
So what do they have in common? I looked at genres first. Casual games show up more often on the underrated list than on Steam in general.
Strategy, simulation and RPGs show up a third as often, or less. My guess? Those genres have fans who go digging for new games.

@scene compareBars {"title": "Who do you play it with?", "aLabel": "100 most underrated", "bLabel": "random Steam games", "rows": [{"label": "Single-player", "a": 0.97, "b": 0.906}, {"label": "Multiplayer", "a": 0.19, "b": 0.362}, {"label": "Online PvP", "a": 0.02, "b": 0.212}], "note": "Steam store categories · same samples"}
Almost all of them are single-player. But so are most Steam games. The real gap is online PvP.
Two percent of the underrated games have it. Twenty-one percent of random Steam games do.
Multiplayer games spread because your friends drag you in. Nobody drags you into a puzzle game.

@scene bigNumber {"value": 0.05, "kind": "pct", "label": "of the 100 most underrated cost $20 or more", "sub": "vs 17% of top-rated games that hit their expected reviews", "color": "accent"}
And they're cheap. Only five percent of them cost twenty dollars or more. Among top-rated games that hit their expectations, it's seventeen percent.
I can't prove why from this data. My guess: cheap often means a tiny team with no marketing budget.

@chapter Honorable mentions
@scene leaderboard @ref:board_hm
Before the top five, a few that just missed the top ten. The Lands of Dream. World End Economica. Nightmares from the Deep. Tin Star.

@scene launchCollision @ref:collision_251490 {"caption": "Same day: Dying Light"}
And number twelve, Gravity Ghost, which launched on the exact same day as Dying Light. Dying Light has four hundred and fifty-seven thousand reviews. Gravity Ghost has three hundred and two.

@chapter #5 to #2
@scene gameCard @ref:card_385250
The top five. Number five. Paint it Back. You solve logic puzzles to restore pixel art.
Ninety-eight percent positive. The model expected over four thousand reviews. It has five hundred and forty-two. Eight times short.

@scene gameCard @ref:card_344480
Number four. Quell. A calm logic puzzle game for four dollars.
Ninety-seven percent positive. The model expected about thirty-five hundred reviews. It has four hundred and thirty-eight.
It came out four days before The Witcher 3. Good story. But remember, not the pattern.

@scene gameCard @ref:card_333260
Number three. Marvin's Mittens. No enemies, no danger. You just explore.
Ninety-five percent positive. The model expected almost eighteen hundred reviews. It has two hundred and five. Eight point six times short.

@scene gameCard @ref:card_496350
Number two is a visual novel. Supipara, Chapter One. Ninety-eight percent positive. That's the highest rating in the top ten.
The model expected about twenty-seven hundred reviews. It has two hundred and fifty-five. Ten point six times short.

@scene bigNumber {"value": 0.34, "kind": "pct", "label": "of its English reviews arrived in the last 2 years", "sub": "released July 2016", "color": "good"}
And here's the strange part. A third of its English reviews came in the last two years. People are still finding it, ten years later.

@chapter #1
@scene scatter @ref:scatter_hero_trend
Number one. Remember the red dot from the start? Ninety-seven percent liked it. Two hundred and eight reviews.
My model expected about twenty-five hundred. That's twelve point three times short. The biggest gap on the list.

@scene textBeat {"text": "It's a *solitaire* game.", "size": 110}
And it's a solitaire game. [pause 0.5]

@scene gameCard @ref:card_570490
SHENZHEN SOLITAIRE, by Zachtronics. It started as a mini-game inside another Zachtronics game, SHENZHEN I/O, then got released on its own for three dollars.
Its store page calls it simple, challenging, and oddly addictive. Ninety-seven percent of players agree.

@scene lineChart @ref:hero_history
This is every month of its life on Steam. It never really spiked. A few English reviews a month, for years.
Should have: about twenty-five hundred reviews. Got: two hundred and eight.

@chapter What did the model miss?
@scene textBeat {"text": "Which game did my model *miss*?", "sub": "Next: the most OVERRATED game on Steam"}
That's the list. Your favourite hidden gem probably isn't on it. Tell me which game my model missed.
Next time I'm flipping the model around: the most overrated game on Steam. That one's going to start some fights.
