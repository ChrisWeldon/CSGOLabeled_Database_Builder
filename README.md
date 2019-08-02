# CS:GO Labeled Match Database

*Database is in production, release will become available upon 700 data points. View production logs [here](http://csgo.chriswevans.com/)
I you would like to have an early release just email me at cwevans612@gmail.com*


All code written by Chris Evans and can be found here at (https://github.com/ChrisWeldon/CSGOLabeled_Database_Builder)
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

`augury.players`

Feature | Type | Description
---|---|---
`PMID`  | int(11) | **Primary Key** Player Match ID
`player_name` | varchar(50) | The players name
`player_id` | varchar(50) | HLTV.org id
`rating2` | float(3,2) | HLTV.org Rating 2.0
`rating1` | float(3,2) | HTLV.org Rating 1.0
`ks_per_rnd` | float(4,2) | Players average kills per round
`assists_per_rnd` | float(4,2) | Players average assists per round
`saved_by_teammate_per_rnd` | float(4,2) | Players average saved by teammate per round
`saves_per_rnd` | float(4,2) | Players average saves per round
`headshots` | float(4,3) | Players average headshots per round
`maps_played` | int(11) | Total maps played
`deaths_per_rnd` | float(4,2) | Players average deaths per round
`age` | int(11) | Players age
`country` | int(11) | Players country of origin
`total_ks` | int(11) | Players total kills
`total_deaths` | int(11) | Players total deaths
`k_death_ratio` | float(3,2) | Players kill to death ratio
`damage_per_rnd` | float(4,2) | Players average damage per round
`grenade_per_rnd` | float(4,2) | Players average grenade damage per round
`rnds_played` | int(11) | Players total rounds played
`rnds_with_ks` | int(11) | Players total rounds where he has scored a kill
`_0_k_rnds` | int(11) | Players total rounds with 0 kills
`_1_k_rnds` | int(11) | Players total rounds with 1 kills
`_2_k_rnds` | int(11) | Players total rounds with 2 kills
`_3_k_rnds` | int(11) | Players total rounds with 3 kills
`_4_k_rnds` | int(11) | Players total rounds with 4 kills
`_5_k_rnds` | int(11) | Players total rounds with 5 kills
`rifle_ks` | int(11) | Players total rifle kills
`sniper_ks` | int(11) | Players total sniper kills
`smg_ks` | int(11) | Players total smg kills
`pistol_ks` | int(11) | Players total pistol kills
`grenade_ks` | int(11) | Players total grenade kills
`other_ks` | int(11) | Players total kills in other ways
`opening_ks` | int(11) | Players total opening kills
`opening_deaths` | int(11) | Players totall opening deaths
`opening_k_ratio` | float(4,2) | Players opening k ratio
`opening_k_rating` | float(4,2) | TBD
`team_win_percent_after_first_k` | float(4,3) |  The win percentage that is achieved after he gets first kill
`first_k_in_won_rounds` | float(4,3) | Number of times he has gotten first kill in won rounds
`date_collected` | datetime | Date collected
`clutch_1v1_w` | int(11) | Total wins alone agains 1 players
`clutch_1v2_w` | int(11) | Total wins alone agains 2 players
`clutch_1v3_w` | int(11) | Total wins alone agains 3 players
`clutch_1v4_w` | int(11) | Total wins alone agains 4 players
`clutch_1v5_w` | int(11) | Total wins alone agains 5 players
`clutch_1v1_l` | int(11) | Total losses alone agains 1 players

## Data Collection

All the data collection was written in Python with BeautifulSoup4 and Mysql-connector. Had I been smart, I would have used Django and used their models and admin library but I'm not so I didn't.

There are 3 main Modules :
 - DatabaseInterface.py: The class solely interacts with MySQL server sitting on beybladematch.com. It is responsible from the addition and deletion of data points, as well as reading data.
 - Scraper.py: Which is does all the data scraping off of HLTV.org.
 - Logger.py: Which is a custom logger class that prints things all fancy like as well as writes to readable .log files for debugging.


There are two processes:
 - load_upcoming.py: Which is responsible for finding all the matches that happen soon, scraping the Features, and saving them into a mysql database
 - load_results.py: Which is responsible for getting the labels and updating the database after a match has finished.

 Wrap those two main process up in a systemd service and bob's your uncle.


## Error Handling

huge part of this is making sure that the database is always collecting data. To do that I need to meticulously error handling and mitigate any process breaking bug.

The first thing was writing a nice Logger.py class and hosting all the log files on a webpage http://csgo.chriswevans.com so I can always tap in and see whats going on with the services.

The next thing was wrapping unanticipated errors with more generic custom errors as they bubble up. For example: If for some reason the data for a player cannot be scraped, then it must be handled at the match collection level where the datapoint can be completely purged. The main processes are only designed to handle anticipated errors like PlayerDataUnscrapableException. If this exception happens then we know exactly what to do, purge the data and try again in 20 minutes when more info may come to light on the datasource.

I can never anticipate every error, but I can make sure that it handled in a wrapper class and log the error to be fixed later.
