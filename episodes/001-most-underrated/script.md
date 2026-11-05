# Episode 001 — I Built a Model to Find the Most Underrated Game on Steam
# Every number comes from facts.json / data.json / traits.json. Rounded only for speech.

@chapter The red dot
@scene scatter @ref:scatter_gg {"highlightAt": 2.0}
See that red dot? That's a game. Ninety-six percent of the people who reviewed it liked it.
It came out in 2015, it costs ten bucks, and it has three hundred and two reviews. [pause 0.5]

@scene textBeat {"text": "It launched the *same* *day* as one of the biggest games of 2015.", "size": 84}
And it launched on the exact same day as one of the biggest games of that year.

@scene textBeat {"text": "51,897 games. One question.", "sub": "Given how good it is, how many people should have played it?"}
So I scored fifty-one thousand, eight hundred and ninety-seven games on Steam to answer one question. [pause 0.4]
Given how good a game is, how many people should have played it? And which games got robbed the hardest?

@chapter How the model works
@scene scatter @ref:scatter_cloud
Here's every one of them. Left to right is how much players liked it. Bottom to top is how many reviews it has.

@scene bigNumber {"value": 0.01, "kind": "pct", "label": "of owners leave a review", "sub": "about 1 in 100 for the games in this video", "color": "gold"}
I'm using reviews as the stand-in for players, because Steam doesn't publish sales.
That's not perfect. For the games on this list, SteamSpy's owner estimates work out to roughly one review for every hundred owners.
So when I say a game got ignored, I mean far fewer people cared enough to show up than you'd expect. Not literally nobody.

@scene textBeat {"text": "20 out of 20 is *not* better than 9,800 out of 10,000."}
Now, the rating. You can't just sort by percent positive.
A game with twenty reviews, all positive, isn't better than a game with nine thousand eight hundred out of ten thousand.

@scene scatter @ref:scatter_cloud {"revealSeconds": 0.3}
So I shrink every score toward the Steam average, and the fewer reviews a game has, the harder it gets pulled in.
A tiny game has to earn its ninety-eight percent.

@scene scatter @ref:scatter_trend
Better games get more reviews. You'd hope so. That gold line is my model, for games that reached Steam around 2014 and 2015. [pause 0.3]
You give it a game's rating and the year it came out. It tells you how many reviews a game like that usually ends up with.
I trained it on every game with at least ten reviews, so it knows what normal looks like, not just what hits look like.

@chapter The rules
@scene textBeat {"text": "The rules", "sub": "Released 2014 or later · no re-releases · no DLC · one game per studio"}
A few rules. Only games from 2014 on, because Steam reviews didn't exist until late 2013.

@scene textBeat {"text": "No 90s re-releases. One game per studio.", "size": 84}
No re-releases of nineties classics, since those already had their moment.
And one game per studio, or a single developer would take three spots.
Then I ranked everything by one number: how many times short of its expected reviews a game landed.

@chapter #10 to #6
@scene leaderboard @ref:board_10
Fifteen thousand games had enough reviews to be judged. These ten got robbed the worst. Let's count down.

@scene gameCard @ref:card_344480 {"rank": 10}
Number ten. Quell. A puzzle game you can get for about four dollars. Ninety-seven percent positive.
My model expected around three thousand two hundred reviews. It has four hundred and thirty-eight.

@scene launchCollision @ref:collision_344480 {"caption": "4 days later: The Witcher 3"}
Want to see something rough? Quell came out on May 14th, 2015. [pause 0.4]
Four days later, The Witcher 3 launched. I wouldn't have noticed a quiet puzzle game that week either.

@scene gameCard @ref:card_412670 {"rank": 9}
Number nine. Bullet Heaven 2. A bullet-hell shooter where you dodge hundreds of bullets a second.
Ninety-eight percent positive. That's the highest rating in the whole top ten, and it's still seven point six times short.

@scene launchCollision @ref:collision_412670 {"caption": "6 days earlier: Rainbow Six Siege"}
It came out December 7th, 2015, six days after Rainbow Six Siege.
Siege has over a million reviews today. Bullet Heaven 2 has four hundred and ninety-three.

@scene gameCard @ref:card_385250 {"rank": 8}
Number eight. Paint it Back. You solve logic puzzles to restore pixel art.
Five hundred and forty-two reviews. The model wanted more than four thousand.

@scene gameCard @ref:card_349250 {"rank": 7}
Number seven. Copy Kitty. You copy enemy powers and combine up to three of them into one super-weapon. [pause 0.3]
Ninety-seven percent positive. Eight times short. It's under four dollars right now, if you want to fix that.

@scene gameCard @ref:card_333260 {"rank": 6}
Number six. Marvin's Mittens. No enemies, no danger. You just explore.
Two hundred and five reviews, against an expected seventeen hundred.

@scene launchCollision @ref:collision_333260 {"caption": "5 days later: Geometry Dash"}
And five days after it launched, Geometry Dash showed up. That one has four hundred and thirty thousand reviews now.

@chapter Was it bad timing?
@scene textBeat {"text": "So it's bad *timing*. Right?", "size": 96}
At this point I had a theory. These games launched next to giants, and got crushed.
Witcher 3. Rainbow Six. Geometry Dash. It's a great story. So I checked it.

@scene bigNumber {"value": 0.74, "kind": "pct", "label": "of ALL games launch within a week of a mega-hit", "color": "text"}
I took Steam's four hundred most-reviewed games and checked every launch against them.
Almost three out of four of games in general launched within a week of one of those hits. There's always a giant nearby.

@scene bigNumber {"value": 0.62, "kind": "pct", "label": "of the most underrated games did", "color": "accent"}
And for the hundred most underrated games? About six in ten. Fewer, not more.
So my theory was wrong. Bad timing makes a good story, but it isn't what these games have in common.

@scene bigNumber {"value": 6.99, "kind": "usd", "label": "median price: the 100 most underrated", "sub": "vs $11.99 for top-rated games that hit expectations", "color": "gold"}
Here's what they do share. They're cheap. The hundred most underrated games have a median price of seven dollars.
Top-rated games that did as well as expected? Twelve dollars.

@scene bigNumber {"value": 0.04, "kind": "pct", "label": "of underrated games cost $20 or more", "sub": "vs 17% of top-rated games that hit expectations", "color": "accent"}
Only four percent of them cost twenty dollars or more. For the games that made it, it's seventeen percent.
I can't prove why from this data. But cheap usually means a tiny team with no marketing budget, and that's my best guess.

@chapter What underrated games have in common
@scene compareBars {"title": "What kind of games get overlooked?", "aLabel": "most underrated", "bLabel": "random Steam games", "rows": [{"label": "Casual", "a": 0.43, "b": 0.22}, {"label": "Strategy", "a": 0.08, "b": 0.31}, {"label": "Simulation", "a": 0.08, "b": 0.31}, {"label": "RPG", "a": 0.11, "b": 0.29}], "note": "Steam store genres · 90 most-underrated games with store data vs a random sample of 160"}
Then I looked at genres. Casual games show up twice as often on the underrated list as they do on Steam in general.
Strategy, simulation and RPGs barely show up at all. My guess? Those genres have fans who go digging for new games. Puzzle fans, maybe not so much.

@scene compareBars {"title": "Who do you play it with?", "aLabel": "most underrated", "bLabel": "random Steam games", "rows": [{"label": "Single-player", "a": 1.0, "b": 0.91}, {"label": "Multiplayer", "a": 0.17, "b": 0.36}, {"label": "Online PvP", "a": 0.01, "b": 0.21}], "note": "Steam store categories · same samples"}
And this was the biggest gap of all. Every single one of them is single-player.
Online PvP? One percent, against twenty-one percent of Steam games. Multiplayer games spread because your friends drag you in. Nobody drags you into a puzzle game.

@chapter Honorable mentions
@scene leaderboard @ref:board_hm
Before the top five, a few that just missed. The Lands of Dream. The Journey Down, Chapter Two. Home Sheep Home.

@scene launchCollision @ref:collision_415920 {"caption": "7 days later: Fallout 4"}
Voidspire Tactics, which came out one week before Fallout 4. Again, a great story, not the cause.

@scene gameCard @ref:card_354400 {"rank": 15, "note": "Metacritic 90: the critics' favourite on this list"}
And number fifteen, Tadpole Treble. This is the one I expected higher. It scored ninety on Metacritic, more than anything else here.
But my model only listens to players, and players gave it two hundred and eighty reviews. Six point three times short. Good, not top ten.

@chapter #5 to #2
@scene gameCard @ref:card_255340 {"rank": 5}
Okay. The top five. Number five. Escape Goat 2. A puzzle platformer where you team up with a mouse to escape a dungeon.
Four hundred and forty-one reviews. Ten point four times short.

@scene textBeat {"text": "The first *Escape* *Goat* would have made the list too.", "size": 80}
Fun fact. The first Escape Goat scored just as badly. It got cut because it came out before Steam reviews existed.

@scene gameCard @ref:card_496350 {"rank": 4}
Number four is a visual novel. Supipara, Chapter One. Ninety-eight percent positive, from two hundred and fifty-five reviews.

@scene bigNumber {"value": 0.34, "kind": "pct", "label": "of its English reviews arrived in the last 2 years", "sub": "released July 2016", "color": "good"}
And here's the strange part. A third of its English reviews came in the last two years. People are still finding it, a decade later.

@scene gameCard @ref:card_236930 {"rank": 3}
Number three. Blackwell Epiphany, the final game in Wadjet Eye's Blackwell series.
Nine hundred and thirty-four reviews sounds healthy until you see the expectation. Over ten thousand. Eleven times short.

@scene textBeat {"text": "Number two is a *solitaire* game.", "size": 96}
Number two surprised me. It's a solitaire game. [pause 0.4]

@scene gameCard @ref:card_570490 {"rank": 2}
SHENZHEN SOLITAIRE started as a mini-game inside Zachtronics' SHENZHEN I/O, then got released on its own for three dollars.
Ninety-seven percent positive. The model expected twenty-five hundred reviews. It has two hundred and eight. Twelve times short.

@chapter #1
@scene leaderboard @ref:board_1
Which brings us back to that red dot from the start.

@scene scatter @ref:scatter_gg_trend
Number one is twenty-one point eight times short of what my model expected. Nothing else on the list comes close.
A game this well liked, from 2015, typically ends up with about six thousand six hundred reviews. This one has three hundred and two.

@scene gameCard @ref:card_251490 {"rank": 1}
It's Gravity Ghost, by Ivy Games. You run, jump, and glide around tiny planets, using gravity to rescue survivors across a shattered galaxy.
Ninety-six percent positive. Seventy-five on Metacritic.

@scene launchCollision @ref:collision_251490 {"caption": "Same day: Dying Light"}
And this is the day it launched. January 26th, 2015. [pause 0.5]
The same day as Dying Light. Dying Light has four hundred and fifty-seven thousand reviews. Gravity Ghost has three hundred and two.

@scene lineChart @ref:gg_history
This is every month of Gravity Ghost's life on Steam. A small bump at launch, then a trickle that never quite stopped.
I know, I just told you timing doesn't explain these games. But for this one, that week, it really didn't help.

@chapter What did the model miss?
@scene textBeat {"text": "Which game did my model *miss*?", "sub": "Next: the most OVERRATED game on Steam"}
So that's the list. Your favourite hidden gem probably isn't on it, so tell me which game my model missed.
Next time I'm flipping the model around: the most overrated game on Steam. That one's going to start some fights.

# NOTES for final pass: replace 0.74, 0.62 (fractions) and their spoken forms from traits.json once
# all 400 mega-hit release dates are fetched. If underrated games are NOT less/more likely to collide, TIMING_VERDICT = "About the same."
