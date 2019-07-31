import mysql.connector
import datetime
from Exceptions import *
from Scraper import *
import sys, json
from Logger import Logger
"""
Rebuilt version of databaseInteractor

This class is specific to reading the augury database.


"""

li = Logger(name="DBI")

class DatabaseInterface:
    def __init__(self):
        with open('config.json', 'r') as json_file:
            text = json_file.read()
            json_data = json.loads(text)
            self.config = json_data
        self.check_time_hours = 1
        self.cnx = mysql.connector.connect(user=self.config["database"]["user"], password=self.config["database"]["password"],
                                      host=self.config["database"]["host"],
                                      database= (self.config["database"]["dev_database_name"] if self.config["dev"]=="True" else self.config["database"]["database_name"]))
        li.log("DatabaseInterface Initialized")

    def __del__(self):
        li.log('DatabaseInterface instance is getting closed')
        self.cnx.close()


    # SELECT name, datum
    # FROM tasks
    # WHERE datum >= NOW()
    def checkUpcomingMatchInDatabase(self, match_id):
        cursor = self.cnx.cursor()
        query_match = ("SELECT match_id, date_start FROM matches WHERE match_id = '"+ match_id +"';")
        cursor.execute(query_match)
        try:
            m = cursor.fetchall()[0]
            match_id = m[0]
            date_start = m[1]
            cursor.close()
            return date_start
        except IndexError:
            cursor.close()
            return False

    def purgeMatch(self, mtid, complete=False):
        li.log("Purging match with MTID " + str(mtid), type='attempt')
        purge_base_dataset = "matches"
        if complete==True:
            purge_base_dataset = "matches_complete"
        cursor = self.cnx.cursor()
        match_query = ("SELECT MTID, t1_GPMID, t2_GPMID from "+purge_base_dataset+" WHERE MTID = " + str(mtid) + ";")
        li.log("Getting GPMID's from " + purge_base_dataset)
        cursor.execute(match_query)
        try:
            match = cursor.fetchall()[0]
        except IndexError:
            li.log("No Match in `match` with mtid " +str(mtid)+ "")
            return
        t1_GPMID = match[1]
        t2_GPMID = match[2]
        t1_GPMID_query = ("SELECT p1, p2, p3, p4, p5 FROM groups WHERE GPMID = " +str(t1_GPMID)+ ";")
        t2_GPMID_query = ("SELECT p1, p2, p3, p4, p5 FROM groups WHERE GPMID = " +str(t2_GPMID)+ ";")
        li.log("Getting PMID's from first group")
        cursor.execute(t1_GPMID_query)
        try:
            t1_group = cursor.fetchall()[0]
        except IndexError:
            li.log("No group data left for first group")
        li.log("Getting PMID's from second group")
        cursor.execute(t2_GPMID_query)
        try:
            t2_group = cursor.fetchall()[0]
        except IndexError:
            li.log("No Group data left for second group")
            match_remove = ("DELETE FROM "+purge_base_dataset+" WHERE MTID = " + str(mtid)+ ";")
            li.log("Deleting match")
            cursor.execute(match_remove)
            self.cnx.commit()
            cursor.close()
            li.log("MTID on " +purge_base_dataset+ " for " +str(mtid)+ " complete")
            return

        # player_query  = ("SELECT player_id from players WHERE PMID in (%s,%s,%s,%s,%s)  ;") # Delete
        # cursor.execute(player_query, t1_group)
        # cursor.execute(player_query, t2_group)
        try:
            player_remove = ("DELETE FROM players WHERE PMID in (%s,%s,%s,%s,%s);") # Delete
            li.log("Deleting players from: " + str(t1_group))
            cursor.execute(player_remove, t1_group)
            li.log("Deleting players from: "+ str(t2_group))
            cursor.execute(player_remove, t2_group)
            group_remove = ("DELETE FROM groups WHERE GPMID in (%s, %s);")
            li.log("Deleting both groups")
            cursor.execute(group_remove, (str(t1_GPMID), str(t2_GPMID)))
            match_remove = ("DELETE FROM "+purge_base_dataset+" WHERE MTID = " + str(mtid)+ ";")
            li.log("Deleting match")
            cursor.execute(match_remove)
            self.cnx.commit()
        except Exception as err:
            li.log(traceback.format_exc, type='traceback')
            li.log(type(err) + ": Purging match with MTID " + str(mtid) + " failed", type="error")
        else:
            li.log("MTID on " +purge_base_dataset+ " for " +str(mtid)+ " complete", type='success')
        finally:
            cursor.close()

    def purgeGroup(self, gpmid):
        li.log("Purging group with GPMID " + str(gpmid), type='attempt')
        try:
            cursor = self.cnx.cursor()
            GPMID_query = ("SELECT p1, p2, p3, p4, p5 FROM groups WHERE GPMID = " +str(gpmid)+ ";")
            cursor.execute(GPMID_query)
            group = cursor.fetchall()[0]
            player_remove = ("DELETE FROM players WHERE PMID in (%s,%s,%s,%s,%s);") # Delete
            li.log("Deleting players from: " + str(group))
            cursor.execute(player_remove, group)
            group_remove = ("DELETE FROM groups WHERE GPMID = "+str(gpmid)+";")
            cursor.execute(group_remove)
            self.cnx.commit()
        except Exception as err:
            li.log(traceback.format_exc(), type='traceback')
            li.log(type(err) + ": Purging group with GPMID " + str(gpmid) + " failed", type='error')
        else:
            li.log("Purging group with GPMID " + str(gpmid) + " success", type='success')
        finally:
            cursor.close()

    def purgePlayer(self, pmid):
        try:
            li.log("Purging player PMID "+ str(pmid), type='attempt')
            cursor = self.cnx.cursor()
            player_remove = ("DELETE FROM players WHERE PMID = "+str(pmid)+";")
            cursor.execute(player_remove)
            self.cnx.commit()
        except Exception as err:
            li.log(traceback.format_exc(), type='traceback')
            li.log(type(err) + ": Purging player PMID "+ str(pmid) + " failed", type='error')
        else:
            li.log("Purging player PMID "+ str(pmid) + " success", type='success')
        finally:
            cursor.close()

    def purgeMatchComplete(self, mtid):
        self.purgeMatch(mtid, complete=True)

    def checkWriteResults(self):
        cursor = self.cnx.cursor()
        query = ("SELECT MTID, match_id, date_start FROM matches WHERE DATE_ADD(NOW(), INTERVAL " + str(self.check_time_hours)+ " HOUR) >= date_start")
        cursor.execute(query)
        for row in cursor.fetchall():
            mtid = row[0]
            match_id = row[1]
            date_start = row[2]
            status_match = getMatchOver(match_id)
            #li.log(str(status_match) + " -  "+ str(match_id)+ " - "+ str(date_start))
            if status_match == "MO": #match over
                #collect results
                copy = ("INSERT INTO matches_complete(MTID, match_id, t1_GPMID, t2_GPMID, match_type, date_start, date_collected) SELECT MTID, match_id, t1_GPMID, t2_GPMID, match_type, date_start, date_collected from matches WHERE MTID='" + str(mtid) + "';")
                cursor.execute(copy)
                self.cnx.commit()
                data = getResultMatchData(match_id)
                add_results = (
                        "UPDATE matches_complete SET"
                        """
                        t1_win = %s,
                        t1_overall_score = %s,
                        t2_overall_score = %s,
                        map_1 = %s,
                        map1_t1_score = %s,
                        map1_t2_score = %s,
                        map1_t1_win = %s,
                        map_2 = %s,
                        map2_t1_score = %s,
                        map2_t2_score = %s,
                        map2_t1_win = %s,
                        map_3 = %s,
                        map3_t1_score = %s,
                        map3_t2_score = %s,
                        map3_t1_win = %s,
                        map_4 = %s,
                        map4_t1_score = %s,
                        map4_t2_score = %s,
                        map4_t1_win = %s,
                        map_5 = %s,
                        map5_t1_score = %s,
                        map5_t2_score = %s,
                        map5_t1_win = %s
                        """
                        "WHERE MTID = '" + str(mtid) +"'")

                t1_wins = 0
                t2_wins = 0

                try:
                    if data["t1_map1_win"] == True:
                        t1_wins += 1
                    elif data["t1_map1_win"] == False:
                        t2_wins += 1
                    else:
                        data["map1"] = None
                        data["t1_map1_win"] = None
                        data["t1_map1_score"] = 0
                        data["t2_map1_score"] = 0
                except KeyError:
                    data["map1"] = None
                    data["t1_map1_win"] = None
                    data["t1_map1_score"] = 0
                    data["t2_map1_score"] = 0

                try:
                    if data["t1_map2_win"] == True:
                        t1_wins += 1
                    elif data["t1_map2_win"] == False:
                        t2_wins += 1
                    else:
                        data["map2"] = None
                        data["t1_map2_win"] = None
                        data["t1_map2_score"] = 0
                        data["t2_map2_score"] = 0
                except KeyError:
                    data["map2"] = None
                    data["t1_map2_win"] = None
                    data["t1_map2_score"] = 0
                    data["t2_map2_score"] = 0

                try:
                    if data["t1_map3_win"] == True:
                        t1_wins += 1
                    elif data["t1_map3_win"] == False:
                        t2_wins += 1
                    else:
                        data["map3"] = None
                        data["t1_map3_win"] = None
                        data["t1_map3_score"] = 0
                        data["t2_map3_score"] = 0
                except KeyError:
                    data["map3"] = None
                    data["t1_map3_win"] = None
                    data["t1_map3_score"] = 0
                    data["t2_map3_score"] = 0

                try:
                    if data["t1_map4_win"] == True:
                        t1_wins += 1
                    elif data["t1_map4_win"] == False:
                        t2_wins += 1
                    else:
                        data["map4"] = None
                        data["t1_map4_win"] = None
                        data["t1_map4_score"] = 0
                        data["t2_map4_score"] = 0
                except KeyError:
                    data["map4"] = None
                    data["t1_map4_win"] = None
                    data["t1_map4_score"] = 0
                    data["t2_map4_score"] = 0

                try:
                    if data["t1_map5_win"] == True:
                        t1_wins += 1
                    elif data["t1_map5_win"] == False:
                        t2_wins += 1
                    else:
                        data["map5"] = None
                        data["t1_map5_win"] = None
                        data["t1_map5_score"] = 0
                        data["t2_map5_score"] = 0
                except KeyError:
                    data["map5"] = None
                    data["t1_map5_win"] = None
                    data["t1_map5_score"] = 0
                    data["t2_map5_score"] = 0

                data["t1_overall_score"] = t1_wins
                data["t2_overall_score"] = t2_wins
                data["t1_win"] = t1_wins > t2_wins


                add_results_data = (
                    data["t1_win"],
                    int(data["t1_overall_score"]),
                    int(data["t2_overall_score"]),
                    data["map1"],
                    int(data["t1_map1_score"]),
                    int(data["t2_map1_score"]),
                    data["t1_map1_win"],
                    data["map2"],
                    int(data["t1_map2_score"]),
                    int(data["t2_map2_score"]),
                    data["t1_map2_win"],
                    data["map3"],
                    int(data["t1_map3_score"]),
                    int(data["t2_map3_score"]),
                    data["t1_map3_win"],
                    data["map4"],
                    int(data["t1_map4_score"]),
                    int(data["t2_map4_score"]),
                    data["t1_map4_win"],
                    data["map5"],
                    int(data["t1_map5_score"]),
                    int(data["t2_map5_score"]),
                    data["t1_map5_win"]
                )
                try:
                    cursor.execute(add_results, add_results_data)
                    self.cnx.commit()
                except Exception as err:
                    raise DatabaseInterfaceCommitException(err)
                remove_match = ("DELETE FROM matches WHERE MTID = " + str(mtid) + ";")
                cursor.execute(remove_match)
                self.cnx.commit()
            elif status_match =="LI": #live
                #leave it be
                pass
            else:
                self.purgeMatch(mtid)
                pass
            cursor.close()

    def writeMatch(self, match_id):
        li.log("------------------ "+ str(match_id.split("/")[2])+" -----------------")
        cursor = self.cnx.cursor()
        try:
            data = getMatchData(match_id)
        except MatchDataUnscrapableException as err:
            li.log(traceback.format_exc(), type="traceback")
            return

        t1_lineup = data['team_1']['players']
        t2_lineup = data['team_2']['players']
        if len(t1_lineup) != 5 or len(t2_lineup) != 5:
            cursor.close()
            raise LineupIncompleteException("Total lineup not 10")
        try:
            t1 = self.writeGroup(data['team_1']['team_id'],t1_lineup)
        except WriteGroupException as err:
            li.log(traceback.format_exc(), type='traceback')
            li.log("failed to write team1 data for match "+ str(match_id))
            cursor.close()
            return
        try:
            t2 = self.writeGroup(data['team_2']['team_id'],t2_lineup)
        except WriteGroupException as err:
            li.log(traceback.format_exc(), type='traceback')
            li.log("failed to write team2 data for match "+ str(match_id))
            self.purgeGroup(t1) #Unable to write group data for t2 so purge the stuff that worked
            cursor.close()
            return

        add_mtid = ("INSERT INTO matches"
                    """(
                    match_id,
                    t1_GPMID,
                    t2_GPMID,
                    match_type,
                    date_start,
                    date_collected
                    )"""
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                    )
        match_type = -1
        if "Best of 1" in data["match_type"] and "(LAN)" not in data["match_type"]:
            match_type = 0
        elif "Best of 2" in data["match_type"] and "(LAN)" not in data["match_type"]:
            match_type = 1
        elif "Best of 3" in data["match_type"] and "(LAN)" not in data["match_type"]:
            match_type = 2
        elif "Best of 5" in data["match_type"] and "(LAN)" not in data["match_type"]:
            match_type = 3
        elif "Best of 1 (LAN)" in data["match_type"]:
            match_type = 4
        elif "Best of 2 (LAN)" in data["match_type"]:
            match_type = 5
        elif "Best of 3 (LAN)" in data["match_type"]:
            match_type = 6
        elif "Best of 5 (LAN)" in data["match_type"]:
            match_type = 7
        mtid_data = (data["match_id"], t1, t2, match_type , datetime.fromtimestamp((int(data["start_datetime"]) / 1e3)), datetime.now())
        try:
            li.log("Writing Match Data to Database")
            cursor.execute(add_mtid, mtid_data)
            self.cnx.commit()
        except Exception as err:
            raise WriteMatchException("Failed to write match data")
        cursor.close()

    #Not open to outside use
    def writeGroup(self, team_id, team_lineup):
        cursor = self.cnx.cursor()
        pmids_lineup = []
        for p in team_lineup:
            try:
                pmids_lineup.append(self.writePlayer(p))
            except WritePlayerException as err:
                li.log("WRITE PLAYER EXCEPTION, UNABLE TO TEST THIS CODE, MONITOR TO SEE IF IT WORKS!!")
                while pmids_lineup:
                    self.purgePlayer(pmids_lineup.pop(-1))
                raise WriteGroupException("WriteGroupException at: " + str(p))
        # try:
        #     p0 = self.writePlayer(team_lineup[0])
        #     p1 = self.writePlayer(team_lineup[1])
        #     p2 = self.writePlayer(team_lineup[2])
        #     p3 = self.writePlayer(team_lineup[3])
        #     p4 = self.writePlayer(team_lineup[4])
        # except WritePlayerException as err:
        #     li.log(err)
        #     raise WriteGroupException("Failed to write player")

        add_gpmid = ("INSERT INTO groups"
                        """(p1,
                        p2,
                        p3,
                        p4,
                        p5,
                        team_id)"""
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        # gpmid_data = (p0,p1,p2,p3,p4, team_id)
        gpmid_data = (pmids_lineup[0],pmids_lineup[1],pmids_lineup[2],pmids_lineup[3],pmids_lineup[4] , team_id)
        try:
            li.log("Writing group data to database")
            cursor.execute(add_gpmid, gpmid_data)
            self.cnx.commit()
        except Exception as err:
            raise WriteGroupException("Failed to write group data, likely a database issue and not the code")

        id = cursor.lastrowid
        cursor.close()
        return id

    #Not open to outside use
    def writePlayer(self, player_id):
        cursor = self.cnx.cursor()
        player_num = player_id.split("/")[0]
        player_name = player_id.split("/")[1]
        try:
            data = getPlayerData(player_num, player_name)
        except PlayerDataUnscrapableException as err:
            raise WritePlayerException("Player data unscrapable for: " + player_id)
        add_pmid = ("INSERT INTO players"
                    """( player_name,
                     player_id,
                     rating2,
                     rating1,
                     ks_per_rnd,
                     assists_per_rnd,
                     saved_by_teammate_per_rnd,
                     saves_per_rnd,
                     headshots,
                     maps_played,
                     deaths_per_rnd,
                     age,
                     country,
                     total_ks,
                     total_deaths,
                     k_death_ratio,
                     damage_per_rnd,
                     grenade_per_rnd,
                     rnds_played,
                     rnds_with_ks,
                     _0_k_rnds,
                     _1_k_rnds,
                     _2_k_rnds,
                     _3_k_rnds,
                     _4_k_rnds,
                     _5_k_rnds,
                     rifle_ks,
                     sniper_ks,
                     smg_ks,
                     pistol_ks,
                     grenade_ks,
                     other_ks,
                     opening_ks,
                     opening_deaths,
                     opening_k_ratio,
                     opening_k_rating,
                     team_win_percent_after_first_k,
                     first_k_in_won_rounds,
                     clutch_1v1_w,
                     clutch_1v1_l,
                     clutch_1v2_w,
                     clutch_1v3_w,
                     clutch_1v4_w,
                     clutch_1v5_w,
                     date_collected
                     )"""
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        #Can't add MTID anyway
        pmid_data = ( player_name,
                    player_id,
                    None if "Rating 2.0" not in data.keys() else float(data["Rating 2.0"]),
                    None if "Rating 1.0" not in data.keys() else float(data["Rating 1.0"]),
                    float(data["Kills / round"]),
                    float(data["Assists / round"]),
                    float(data["Saved by teammate / round"]),
                    float(data["Saved teammates / round"]),
                    float(data["Headshot %"].rstrip("%"))/100,
                    float(data["Maps played"]),
                    float(data["Deaths / round"]),
                    None if "Age" not in data.keys() else None if data["Age"] == "-" else int(data["Age"][:1]),
                    0, # country needs extra table
                    int(data["Kills"]),
                    int(data["Deaths"]),
                    float(data["K/D Ratio"]),
                    float(data["Damage / Round"]),
                    float(data["Grenade dmg / Round"]),
                    int(data["Rounds played"]),
                    int(data["Rounds with kills"]),
                    int(data["0 kill rounds"]),
                    int(data["1 kill rounds"]),
                    int(data["2 kill rounds"]),
                    int(data["3 kill rounds"]),
                    int(data["4 kill rounds"]),
                    int(data["5 kill rounds"]),
                    int(data["Rifle kills"]),
                    int(data["Sniper kills"]),
                    int(data["SMG kills"]),
                    int(data["Pistol kills"]),
                    int(data["Grenade"]),
                    int(data["Other"]),
                    int(data["Total opening kills"]),
                    int(data["Total opening deaths"]),
                    float(data["Opening kill ratio"]),
                    float(data["Opening kill rating"]),
                    float(data["Team win percent after first kill"].rstrip("%"))/100,
                    float(data["First kill in won rounds"].rstrip("%"))/100,
                    int(data["1 on 1 Wins"]),
                    int(data["1 on 1 Losses"]),
                    int(data["1 on 2 Wins"]),
                    int(data["1 on 3 Wins"]),
                    int(data["1 on 4 Wins"]),
                    int(data["1 on 5 Wins"]),
                    datetime.now()
                    )
        try:
            li.log("Writing player data to database")
            cursor.execute(add_pmid, pmid_data)
            self.cnx.commit()
        except MySQLInterfaceError as err:
            raise WritePlayerException("Unable to write player data for " + str(player_id))
        id = cursor.lastrowid      #Collects all player data and creates PMID
        return id

if __name__ == "__main__":
    di = DatabaseInterface()
