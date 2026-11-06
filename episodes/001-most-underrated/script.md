# Episode 001: I Built a Model to Find the Most Underrated Game on Steam (v4: KNN model, Steam-first verified, consensus order)
# Every number comes from facts.json (pipeline/ep001_facts.py) or robustness.json. Rounded only for speech. '|' = line break.

@chapter The red dot
@scene scatter @ref:scatter_hero {"highlightAt": 2.0}
See that red dot? That's a game. Ninety-seven percent of its reviews are positive.
It costs ten dollars... and it has three hundred and two reviews. [pause 0.5]
Games like it usually ended up with about two thousand.

@scene textBeat {"text": "Same launch day as one of|the *biggest* games of 2015.", "sub": "Steam store release dates", "size": 84}
Oh, and it launched on Steam the exact same day as one of the biggest games of twenty fifteen. Hold that thought.

@scene textBeat {"text": "51,897 games. One question."}
I wanted to find the great games that got overlooked the worst. I scored fifty-one thousand, eight hundred and ninety-seven Steam games, all with one question. [pause 0.4]

@scene textBeat {"text": "Given how good it is,|how many people *should* have played it?", "size": 80}
Given how good a game is, how many people should have played it? And which games got robbed the hardest?

@scene scatter @ref:scatter_hero {"highlightAt": 0.3, "revealSeconds": 0.3}
That red dot is on my list. You'll see where at the end.

@chapter How the model works
@scene scatter @ref:scatter_cloud
Here's a sample of those games. Left to right is how much reviewers liked it. Bottom to top is how many reviews it got, and each step up is ten times more.

@scene bigNumber {"value": 130, "kind": "int", "label": "owners for every review", "sub": "typical for the games in this video (SteamSpy estimates)", "color": "gold"}
Steam doesn't publish sales, so I'm using reviews instead. For the games on my list, there's roughly one review for every hundred and thirty owners.

@scene textBeat {"text": "reviews aren't players|but more reviews = *more players*", "size": 84}
Reviews aren't players, and that ratio moves around a lot. But more reviews generally means more players, so it's the best yardstick I've got.

@scene textBeat {"text": "Rating = *% positive*?", "size": 96}
Now, ratings. You can't just sort by percent positive.

@scene textBeat {"text": "20 out of 20 is *not* better|than 9,800 out of 10,000."}
A game with twenty reviews, all positive, isn't better than a game with nine thousand eight hundred out of ten thousand.

@scene textBeat {"text": "every score pulled toward *80%*|fewer reviews = harder pull", "size": 80}
So I pull every score toward the average for games with two hundred or more reviews, which is about eighty percent. The fewer reviews a game has, the harder it gets pulled.

@scene textBeat {"text": "150 games just like it:|same rating, same launch window.", "size": 80}
Here's the model. For every game, I find the hundred and fifty games most like it. Released around the same time, with almost the same rating.

@scene textBeat {"text": "what the typical one got|= *expected*", "size": 96}
Whatever the typical one of those got, that's what I call expected.

@scene scatter @ref:scatter_trend
These are games from the red dot's launch window, around the turn of twenty fifteen. The gold line is what they usually got at each rating. Near the top, the line climbs.

@scene textBeat {"text": "expects 1,000 · has 100|= *10x* short"}
Here's the number I rank by. Say a game's lookalikes usually got a thousand reviews, and it only has a hundred.
That's ten times short. The bigger that number, the harder a game got robbed.

@scene bigNumber {"value": 2.7, "kind": "x1", "label": "typical miss, across all 51,897 games", "sub": "fewer than 1% of games with 200+ reviews are this far short", "color": "text"}
Is this perfect? No. Across all fifty-one thousand games, the prediction is typically off by about two point seven times, one way or the other.

@scene textBeat {"text": "games with 200+ reviews:|fewer than *1 in 100* are this far short", "size": 80}
But for games with two hundred or more reviews it usually guesses low, and fewer than one in a hundred of them is even that far short. So the further past that a game is, the more sure I am it really got robbed.

@scene bigNumber {"value": 7, "kind": "int", "label": "versions of the model", "sub": "same 7 in the top 10 and same 4 in the top 5, every time · among the 16 games that passed every check", "color": "gold"}
And to check I wasn't fooling myself, I ran the model seven different ways. Of the sixteen games that passed every check, the same seven made the top ten every single time, and the same four made the top five.

@scene textBeat {"text": "final order = the *average*|of all 7 versions", "size": 88}
The final order, and every game's times-short number from here on, is the average of all seven.

@chapter The rules
@scene textBeat {"text": "The rules", "sub": "released 2014 or later · 200+ reviews"}
A few rules. Only games released from twenty fourteen on, because Steam reviews didn't exist until late twenty thirteen. At least two hundred reviews, so a handful of fans can't fake it.

@scene textBeat {"text": "No DLC|one game per *studio*", "size": 96}
No DLC. And one game per studio, so no single developer hogs the list.

@scene textBeat {"text": "It has to launch|on *Steam first*", "sub": "or the same day as everywhere else", "size": 96}
And one more rule, which ended up mattering more than anything else. The game has to have launched on Steam first, or at least the same day.

@scene bigNumber {"value": 34, "kind": "int", "label": "of the 51 games I checked had been released somewhere else first", "sub": "browser and Flash games, mobile, older PC versions, Japan", "color": "accent"}
I checked fifty-one of the top candidates by hand. Thirty-four of them had already been out somewhere else. Free Flash games, phone games, games that came out years earlier in Japan.

@scene textBeat {"text": "played somewhere else first|= *not overlooked*", "size": 88}
Those aren't overlooked. Their fans just played them somewhere else first. So they're out.

@chapter #10 to #6
@scene leaderboard @ref:board_10
Numbers ten to six are closer calls. They're about three times short, right around the model's typical miss. Call them probably overlooked.

@scene gapBars @ref:gap_399600
Number ten. A game called "I and Me." Ninety-six percent positive. Games like it usually got about nine hundred reviews. It has three hundred and fifty-eight. Two point six times short.

@scene gapBars @ref:gap_377690
Number nine. Starlight Vega, a visual novel. Ninety-four percent positive, and about two point eight times short.

@scene gapBars @ref:gap_236930
Number eight. Blackwell Epiphany, the final game in Wadjet Eye's Blackwell series.
Ninety-eight percent positive, the highest rating in the whole top ten, and still about three times short.

@scene textBeat {"text": "sequels reach *fewer players*?", "sub": "my guess · 4 of the top 10 are sequels", "size": 88}
One caveat. It's a sequel, like three others on this list, and my guess is that sequels reach fewer players than the first game. So take those with a pinch of salt.

@scene gapBars @ref:gap_389650
Number seven. Stardust Galaxy Warriors, a couch co-op space shooter. Two hundred and twenty-six reviews, against about seven hundred expected. About three times short.

@scene gameCard @ref:card_317320
Number six. Nelly Cootalot: The Fowl Fleet. A pirate point-and-click adventure, and its store page says Tom Baker is in the cast.

@scene gapBars @ref:gap_317320
Eighty-one on Metacritic. Three point two times short.

@chapter Was it bad timing?
@scene textBeat {"text": "So it's bad *timing*.|Right?", "size": 96}
Before the top five, I want to test a theory. Remember that red dot launching next to a giant? Maybe that's the whole story. Good games, buried by bad timing.

@scene bigNumber {"value": 0.716, "kind": "pct", "label": "of popular Steam games launched within a week of a mega-hit", "sub": "mega-hit = one of Steam's 400 most-reviewed games · random sample of 141 games from 2014 on with 300+ reviews · Steam store dates · not matched on rating or year", "color": "text"}
So I took Steam's four hundred most-reviewed games, and checked launch dates against them.
Seven in ten popular Steam games launched within a week of one of those hits. Most of the time, there's a giant nearby.

@scene bigNumber {"value": 0.676, "kind": "pct", "label": "of the underrated-looking games did", "sub": "34 games from 2014 on with 200+ reviews, rated 93%+, two-thirds or less of expected reviews · one per studio · known earlier releases left out, 19 of 34 not release-checked · small sample, not matched on rating or year", "color": "accent"}
Now the underrated-looking games: thirty-four top-rated games that got two-thirds or less of the reviews they should have. Two in three. About the same.
Bad timing makes a good story. But it isn't the pattern.

@chapter What they have in common
@scene compareBars @ref:genres_chart
So what do they have in common? Genre, for one. Compared with popular Steam games, casual games show up more often. Forty-seven percent, against twenty-five.
Strategy and simulation games show up half as often, or less.

@scene textBeat {"text": "19 of these 34 games|*not checked* by hand yet", "size": 88, "sub": "for earlier releases elsewhere"}
One caveat: more than half of these games, nineteen of the thirty-four, I haven't checked by hand yet. Among the fifteen I did check, casual games are a third. Still more than a quarter, but a smaller gap.

@scene textBeat {"text": "strategy and sim fans|go *digging* for new games", "size": 84, "sub": "a guess"}
My guess? Strategy and sim fans go digging for new games, so fewer good ones slip through.

@scene compareBars @ref:players_chart
All of them are single-player. But so are most popular Steam games. The real gap is online player-versus-player.
Just one of the thirty-four has it. More than one in five popular Steam games do.

@scene textBeat {"text": "Nobody drags you into|a *puzzle game*.", "size": 96}
My guess: multiplayer games spread because your friends drag you in. Nobody drags you into a puzzle game.

@scene bigNumber {"value": 0.029, "kind": "pct", "label": "of the underrated-looking games cost $20 or more", "sub": "1 of 34 · vs 22% of popular Steam games · current list prices · groups not matched on rating or year", "color": "accent"}
And they're rarely expensive. Almost none cost twenty dollars or more: just one of the thirty-four. Among popular Steam games, it's more than one in five.

@scene textBeat {"text": "cheap often means a tiny team|with *no marketing budget*", "size": 80, "sub": "a guess, not something this data can prove"}
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

@scene textBeat {"text": "built for *couch play*", "size": 96}
And yes, it's multiplayer. But it's built for couch play, with friends in the same room.

@scene gameCard @ref:card_415920
Number three. Voidspire Tactics, a turn-based tactics RPG where you build your own party.

@scene gapBars @ref:gap_415920
Ninety-seven percent positive. About fourteen hundred expected. Two hundred and sixty-eight reviews. Five point three times short.

@scene launchCollision @ref:collision_415920 {"caption": "Within a week on Steam: Call of Duty, Fallout 4"}
It came out on Steam on November second, twenty fifteen. Within about a week, Call of Duty: Black Ops Three and Fallout 4 both launched. Bad luck? Sure. But remember, not the pattern.

@scene gameCard @ref:card_255340
Number two. Escape Goat 2. A puzzle platformer where you team up with a friendly mouse to get out of a dungeon.

@scene gapBars @ref:gap_255340
Ninety-six percent positive. Almost twenty-nine hundred reviews expected. It has four hundred and forty-one. Six point six times short.

@scene textBeat {"text": "#1 vs #2: *neck and neck*", "sub": "Escape Goat 2 was #1 in 3 of 7 versions of the model", "size": 96}
And honestly? Number one and number two are neck and neck. In three of my seven versions of the model, Escape Goat 2 was number one.

@chapter #1
@scene scatter @ref:scatter_hero_trend
But in the other four, it was this. Remember the red dot? Ninety-seven percent positive. Three hundred and two reviews.
Games like it usually got about two thousand. That's six point six times short.

@scene gameCard @ref:card_251490
It's Gravity Ghost, by Ivy Games. You run, jump and glide from planet to planet using gravity, rescuing survivors across a shattered galaxy.
Critics gave it a seventy-five.

@scene launchCollision @ref:collision_251490 {"caption": "Same day: Dying Light"}
And here's the launch day I told you to hold onto. January twenty-sixth, twenty fifteen, on Steam. [pause 0.5]
The same day as Dying Light. Dying Light has four hundred and fifty-eight thousand reviews.

@scene textBeat {"text": "Same day: Dying Light|3 days later: *Life is Strange*", "size": 84, "sub": "Steam store release dates"}
I know, I just told you timing isn't the pattern. But Dying Light the same day, and Life is Strange three days later on Steam? That week couldn't have helped.

@scene lineChart @ref:hero_history
Here are its English-language reviews, about half of all of them, month by month. A small bump at launch, then a trickle that never quite stopped.

@scene gapBars @ref:gap_251490
It should have had about two thousand reviews. It got three hundred and two.

@chapter What did the model miss?
@scene textBeat {"text": "Which game did my model *miss*?", "sub": "Next: the most OVERRATED game on Steam"}
That's the list. Your favourite hidden gem probably isn't on it. Tell me which game my model missed.
Next time I'm flipping the model around: the most overrated game on Steam. That one's going to start some fights.
