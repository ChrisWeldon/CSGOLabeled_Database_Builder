# CS:GO Labeled Match Database

Code written by Chris Evans can be found here at (https://www.github.com/ChrisWeldon)
Webpage to view the log files can be found here: (http://csgo.chriswevans.com/) and code for the webpage here (https://www.github.com/ChrisWeldon)
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

`GPMID` int(11) NOT NULL,
`p1` int(11) DEFAULT NULL,
`p2` int(11) DEFAULT NULL,
`p3` int(11) DEFAULT NULL,
`p4` int(11) DEFAULT NULL,
`p5` int(11) DEFAULT NULL,
`team_id` varchar(30) DEFAULT NULL


matches

Feature | Type | Description
`MTID` | int(11) | **Primary Key** The Match Time Id
`match_id` | varchar(100) |



`t1_GPMID` | int(11) |
`t2_GPMID` | int(11) |
`match_type` | int(11) |
`map_1` | varchar(100) |
`map_t1_win` | tinyint(1) |
`map_2` | varchar(20) |
`map_t2_win` | tinyint(1) |
`map_3` | varchar(20) |
`map_t3_win` | tinyint(1) |
`map_4` | varchar(20) |
`map_t4_win` | tinyint(1) |
`map_5` | varchar(20) |
`map_t5_win` | tinyint(1) |
`t1_score` | int(11) |
`t2_score` | int(11) |
`t1_win` | tinyint(1) |
`date_start` | datetime |
`date_delay` | datetime |
`date_collected`| date |


CREATE TABLE `matches_complete`
`MTID` int(11) NOT NULL,
`match_id` varchar(100) DEFAULT NULL,
`t1_GPMID` int(11) DEFAULT NULL,
`t2_GPMID` int(11) DEFAULT NULL,
`match_type` int(11) DEFAULT NULL,
`map_1` varchar(100) DEFAULT NULL,
`map1_t1_win` tinyint(1) DEFAULT NULL,
`map_2` varchar(20) DEFAULT NULL,
`map2_t1_win` tinyint(1) DEFAULT NULL,
`map_3` varchar(20) DEFAULT NULL,
`map3_t1_win` tinyint(1) DEFAULT NULL,
`map_4` varchar(20) DEFAULT NULL,
`map4_t1_win` tinyint(1) DEFAULT NULL,
`map_5` varchar(20) DEFAULT NULL,
`map5_t1_win` tinyint(1) DEFAULT NULL,
`t1_score` int(11) DEFAULT NULL,
`t2_score` int(11) DEFAULT NULL,
`t1_win` tinyint(1) DEFAULT NULL,
`date_start` datetime DEFAULT NULL,
`date_delay` datetime DEFAULT NULL,
`date_collected` date DEFAULT NULL,
`t1_overall_score` int(11) DEFAULT NULL,
`t2_overall_score` int(11) DEFAULT NULL,
`map1_t1_score` int(11) DEFAULT NULL,
`map1_t2_score` int(11) DEFAULT NULL,
`map2_t1_score` int(11) DEFAULT NULL,
`map2_t2_score` int(11) DEFAULT NULL,
`map3_t1_score` int(11) DEFAULT NULL,
`map3_t2_score` int(11) DEFAULT NULL,
`map4_t1_score` int(11) DEFAULT NULL,
`map4_t2_score` int(11) DEFAULT NULL,
`map5_t1_score` int(11) DEFAULT NULL,
`map5_t2_score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `players`
`PMID` int(11) NOT NULL,
`player_name` varchar(50) DEFAULT NULL,
`player_id` varchar(50) DEFAULT NULL,
`rating2` float(3,2) DEFAULT NULL,
`rating1` float(3,2) DEFAULT NULL,
`ks_per_rnd` float(4,2) DEFAULT NULL,
`assists_per_rnd` float(4,2) DEFAULT NULL,
`saved_by_teammate_per_rnd` float(4,2) DEFAULT NULL,
`saves_per_rnd` float(4,2) DEFAULT NULL,
`headshots` float(4,3) DEFAULT NULL,
`maps_played` int(11) DEFAULT NULL,
`deaths_per_rnd` float(4,2) DEFAULT NULL,
`age` int(11) DEFAULT NULL,
`country` int(11) DEFAULT NULL,
`total_ks` int(11) DEFAULT NULL,
`total_deaths` int(11) DEFAULT NULL,
`k_death_ratio` float(3,2) DEFAULT NULL,
`damage_per_rnd` float(4,2) DEFAULT NULL,
`grenade_per_rnd` float(4,2) DEFAULT NULL,
`rnds_played` int(11) DEFAULT NULL,
`rnds_with_ks` int(11) DEFAULT NULL,
`_0_k_rnds` int(11) DEFAULT NULL,
`_1_k_rnds` int(11) DEFAULT NULL,
`_2_k_rnds` int(11) DEFAULT NULL,
`_3_k_rnds` int(11) DEFAULT NULL,
`_4_k_rnds` int(11) DEFAULT NULL,
`_5_k_rnds` int(11) DEFAULT NULL,
`rifle_ks` int(11) DEFAULT NULL,
`sniper_ks` int(11) DEFAULT NULL,
`smg_ks` int(11) DEFAULT NULL,
`pistol_ks` int(11) DEFAULT NULL,
`grenade_ks` int(11) DEFAULT NULL,
`other_ks` int(11) DEFAULT NULL,
`opening_ks` int(11) DEFAULT NULL,
`opening_deaths` int(11) DEFAULT NULL,
`opening_k_ratio` float(4,2) DEFAULT NULL,
`opening_k_rating` float(4,2) DEFAULT NULL,
`team_win_percent_after_first_k` float(4,3) DEFAULT NULL,
`first_k_in_won_rounds` float(4,3) DEFAULT NULL,
`date_collected` datetime DEFAULT NULL,
`clutch_1v1_w` int(11) NOT NULL,
`clutch_1v2_w` int(11) NOT NULL,
`clutch_1v3_w` int(11) NOT NULL,
`clutch_1v4_w` int(11) NOT NULL,
`clutch_1v5_w` int(11) NOT NULL,
`clutch_1v1_l` int(11) NOT NULL
