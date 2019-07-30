# CS:GO Labeled Match Database

Code written by Chris Evans can be found here at (https://github.com/ChrisWeldon/CSGOLabeled_Database_Builder)
Webpage to view the log files can be found here: (http://csgo.chriswevans.com/) and code for the webpage here (https://github.com/ChrisWeldon/Augury_Webapp_Client)
All the data is hosted on a mysql server at (http://pma.beybladematch.com), behind a login. Email me if you want one. (The data exists on a server that I use for multiple webpages I've build, forgive the name.)

This code is an attempt to create the first labeled dataset for CS:GO professional match prediction.
As of right now, the code exists on a personal Ubuntu server running the two main pieces: The feature collection, and the label collection.

I also attempted another sister project to this which was to predict the winners of CS:GO professional matches with the data from this set to gain an edge on betting platforms. More on that later...

The main focus of this project is constant error handling and logging. Basically, to have an accurate dataset, It must be running at all times to ensure that it is accurate. The challenge is that the data has tons of human variability in it, so I can't possibly predict all the things that could go wrong. The only possible solution is to log all the errors that occur so that I can write fixes as they come up.

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
 - 1 data point in matches_complete represents one predictable point.
 - 2 groups for every row in matches_complete
 - 5 players for every row in groups

 ### Schema
**`augury.groups`**

Feature | Type | Description
---|---|---
`GPMID` | int(11) | **Primary Key** Group Player Match ID
`p1` | int(11) | PMID for player 1 of group GPMID
`p2` | int(11) | PMID for player 2 of group GPMID
`p3` | int(11) | PMID for player 3 of group GPMID
`p4` | int(11) | PMID for player 4 of group GPMID
`p5` | int(11) | PMID for player 5 of group GPMID
`team_id` | varchar(30) | The HLTV.org Id of the team


**`augury.matches`**

Feature | Type | Description
---|---|---
`MTID` | int(11) | **Primary Key**  Match Time ID
`match_id` | varchar(100) | HLTV.org given match ID
`t1_GPMID` | int(11) | The GPMID for group 1
`t2_GPMID` | int(11) | The GPMID for group 2
`match_type` | int(11) | The match type (0-6) bo1=:0, b02=1, bo3=2, bo5=3, bo1(LAN)=4, bo2(LAN)=5, bo3(LAN)=6,bo5(LAN)=7
`date_start` | datetime | Date the match starts
`date_delay` | datetime | When it was delayed to if delayed (*Deprecated*)
`date_collected`| date | When the Feature data was collected


`augury.matches_complete`

This table is the same as augury.matches only it has the labels as well.

Feature | Type | Description
---|---|---
`MTID` | int(11) | **Primary Key**  Match Time ID (Same as augury.matches)
`match_id` | varchar(100) | HLTV.org given match ID
`t1_GPMID` | int(11) | The GPMID for group 1
`t2_GPMID` | int(11) | The GPMID for group 2
`match_type` | int(11) | The match type (0-6) bo1=:0, b02=1, bo3=2, bo5=3, bo1(LAN)=4, bo2(LAN)=5, bo3(LAN)=6,bo5(LAN)=7
`map_1` | varchar(100) | Name of map 1
`map1_t1_win` | tinyint(1) | If team 1 won map 1
`map_2` | varchar(20) | Name of map 2
`map2_t1_win` | tinyint(1) | If team 1 won map 2
`map_3` | varchar(20) | Name of map 3
`map3_t1_win` | tinyint(1) | If team 1 won map 3
`map_4` | varchar(20) | Name of map 4
`map4_t1_win` | tinyint(1) | If team 1 won map 4
`map_5` | varchar(20) | Name of map 5
`map5_t1_win` | tinyint(1) | If team 1 won map 5
`t1_score` | int(11) | (*Deprecated*)
`t2_score` | int(11) | (*Deprecated*)
`t1_win` | tinyint(1) | If team 1 won the whole match
`date_start` | datetime | Date the match starts
`date_delay` | datetime | When it was delayed to if delayed (*Deprecated*)
`date_collected` | date | When the Feature data was collected
`t1_overall_score` | int(11) | The overall match score that team 1 achieved
`t2_overall_score` | int(11) | The overall match score that team 2 achieved
`map1_t1_score` |  int(11) | Score achieved by team 1 on map 1
`map1_t2_score` |  int(11) | Score achieved by team 2 on map 1
`map2_t1_score` |  int(11) | Score achieved by team 1 on map 2
`map2_t2_score` |  int(11) | Score achieved by team 2 on map 2
`map3_t1_score` |  int(11) | Score achieved by team 1 on map 3
`map3_t2_score` |  int(11) | Score achieved by team 2 on map 3
`map4_t1_score` |  int(11) | Score achieved by team 1 on map 4
`map4_t2_score` |  int(11) | Score achieved by team 2 on map 4
`map5_t1_score` |  int(11) | Score achieved by team 1 on map 5
`map5_t2_score` |  int(11) | Score achieved by team 2 on map 5



CREATE TABLE `players`
`PMID` int(11)
`player_name` varchar(50)
`player_id` varchar(50)
`rating2` float(3,2)
`rating1` float(3,2)
`ks_per_rnd` float(4,2)
`assists_per_rnd` float(4,2)
`saved_by_teammate_per_rnd` float(4,2)
`saves_per_rnd` float(4,2)
`headshots` float(4,3)
`maps_played` int(11)
`deaths_per_rnd` float(4,2)
`age` int(11)
`country` int(11)
`total_ks` int(11)
`total_deaths` int(11)
`k_death_ratio` float(3,2)
`damage_per_rnd` float(4,2)
`grenade_per_rnd` float(4,2)
`rnds_played` int(11)
`rnds_with_ks` int(11)
`_0_k_rnds` int(11)
`_1_k_rnds` int(11)
`_2_k_rnds` int(11)
`_3_k_rnds` int(11)
`_4_k_rnds` int(11)
`_5_k_rnds` int(11)
`rifle_ks` int(11)
`sniper_ks` int(11)
`smg_ks` int(11)
`pistol_ks` int(11)
`grenade_ks` int(11)
`other_ks` int(11)
`opening_ks` int(11)
`opening_deaths` int(11)
`opening_k_ratio` float(4,2)
`opening_k_rating` float(4,2)
`team_win_percent_after_first_k` float(4,3)
`first_k_in_won_rounds` float(4,3)
`date_collected` datetime
`clutch_1v1_w` int(11)
`clutch_1v2_w` int(11)
`clutch_1v3_w` int(11)
`clutch_1v4_w` int(11)
`clutch_1v5_w` int(11)
`clutch_1v1_l` int(11)
