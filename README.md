# CS:GO Labeled Match Database

Code written by Chris Evans can be found here

This code is an attempt to create the first labeled dataset for CS:GO professional match prediction.
As of right now, the code exists on a personal Ubuntu server running the two main pieces: The feature collection, and the label collection.

I also attempted another sister project to this which was to predict the winners of CS:GO professional matches to gain an edge on betting platforms. More on that later...

## Database Architecture

The only data previously available to assist in predicting CS:GO matches was not so great. Mostly because all that consisted in the dataset were labels.
If you are unfamiliar with the game, all you need to know is that the pre existing data only contained the results of the game (ei who won, how many kills, etc) Being someone with relatively week ML skills, having only labels really does not help much because there is no data in which to place the actual prediction. Here is where my project comes in,

I need dataset that contains the stats of all the players playing in a match as well as the results of the match after it has occurred.

All the data will be collected off of HLTV.org, which houses a ton of useful data about matches and who beat who in the past.
All the data is collected using Python and stored in a MySQL server.

### Tables and relations

There are 4 tables: matches, matches_complete, groups, and players.

#### Overview of each table
 - matches : Is all the preliminary data needed from each match, which teams are playing, what time, etc,. Primary key 'MTID' (Match Time ID)
 - matches_complete : Is a copy of matches with the addition of all the label data. Primary Key 'MTID'
 - groups : This table contains all of the PMID's of each team. Primary Key 'GPMID' (Group Player Match ID)
 - players : This table contains the time specific avg. data for each player 20 minutes before the match occurs. Primary Key 'PMID'

#### Relations
