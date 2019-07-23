import mysql.connector
from Scraper import getPlayerData
from Scraper import getMatchData
from Scraper import getMatches
from Scraper import getResultMatchData
import datetime
from src.Exceptions import PlayerDataUnscrapableException
from src.Exceptions import MatchDataUnscrapableException
"""This Class is deprecated...
Riddled with bugs that should just be rewritten, also should not scrape inside the class.""""


##TODO make it update match queue by truncating all but active games and also make it not make multiple MTID's for active maps


class databaseInteractor:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='chris', password='Chris)98',
                                      host='beybladematch.com',
                                      database='augury')
    def __del__(self):
        self.cnx.close()

    def createPMID(self, player_id, c=None): #TODO make PMID object
        print("CREATING PMID FOR: ", player_id)
        if c == None:
            cursor = self.cnx.cursor()
        else:
            cursor = c

        cursor = self.cnx.cursor()
        player_num = player_id.split("/")[0]
        player_name = player_id.split("/")[1]
        data = getPlayerData(player_num, player_name)
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
                     0_k_rnds,
                     1_k_rnds,
                     2_k_rnds,
                     3_k_rnds,
                     4_k_rnds,
                     5_k_rnds,
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
                    None if data["Age"] == "-" else int(data["Age"]),
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
                    datetime.datetime.now()
                    )
        cursor.execute(add_pmid, pmid_data)
        self.cnx.commit()
        id = cursor.lastrowid
        if c == None:
            cursor.close()      #Collects all player data and creates PMID
        return id

    def createMTID(self, match_id, c=None, d=None):    #TODO make MTID Object
        if c == None:
            cursor = self.cnx.cursor()
        else:
            cursor = c
        match_url = 'https://www.hltv.org' + match_id
        print(match_url)
        print(match_id)
        if d == None:
            data = getMatchData(match_id)
        else:
            data = d
        print(data["match_type"])
        t1_lineup = data['team_1']['players']
        t2_lineup = data['team_2']['players']

        if len(t1_lineup) != 5 or len(t2_lineup) != 5:
            raise PlayerDataUnscrapableException("Lineups are not sufficient")
            if c == None:
                cursor.close()
        else:
            t1 = self.createGPMID(t1_lineup, data['team_1']["team_id"], c=cursor)
            t2 = self.createGPMID(t2_lineup, data['team_2']["team_id"], c=cursor)
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
            mtid_data = (match_id, t1, t2, match_type , datetime.datetime.fromtimestamp((int(data["start_datetime"]) / 1e3)), datetime.datetime.now())
            cursor.execute(add_mtid, mtid_data)
            self.cnx.commit()

            if c == None:
                cursor.close()

    def createGPMID(self, lineup, team_id, c=None):
        print(lineup)
        assert(len(lineup) == 5), "Argument must be a list of 5 player ids"
        if c == None:
            cursor = self.cnx.cursor()
        else:
            cursor = c

        p1 = self.createPMID(lineup[0], c=cursor)
        p2 = self.createPMID(lineup[1], c=cursor)
        p3 = self.createPMID(lineup[2], c=cursor)
        p4 = self.createPMID(lineup[3], c=cursor)
        p5 = self.createPMID(lineup[4], c=cursor)

        add_gpmid = ("INSERT INTO groups"
                        """(p1,
                        p2,
                        p3,
                        p4,
                        p5,
                        team_id)"""
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        gpmid_data = (p1,p2,p3,p4,p5, team_id)
        cursor.execute(add_gpmid, gpmid_data)
        self.cnx.commit()
        id = cursor.lastrowid

        if c == None:
            cursor.close()
        return id

    def createMQID(self, match_id, time_start, c=None):
        if c == None:
            cursor = self.cnx.cursor()
        else:
            cursor = c

        add_mqid = ("INSERT IGNORE INTO matchqueue"
                    """(
                    match_id,
                    date_start
                    )"""
                    "VALUES (%s,%s)"
                    )

        mqid_data = (match_id,
                    time_start)
        cursor.execute(add_mqid, mqid_data)
        self.cnx.commit()
        id = cursor.lastrowid
        if c == None:
            cursor.close()
        return id

    def updateMatchQueue(self, c=None):
        if c == None:
            cursor = self.cnx.cursor(buffered=True)
        else:
            cursor = c

        cursor.execute("SELECT * FROM matchqueue WHERE matchqueue.started != 2")
        matches_local = cursor.fetchall()
        matches_online = getMatches()

        #---------------------Checking Local to online---------------------
        print(matches_local)
        for match in matches_local:
            try:
                data = getMatchData(match[1])
            except MatchDataUnscrapableException:
                print(" Match Data Unscrapable ..... Deleting off queue")
                cursor.execute("DELETE FROM matchqueue WHERE matchqueue.match_id = '" + match[1] + "'")
                self.cnx.commit()
                continue

            start_time = datetime.datetime.fromtimestamp((int(data["start_datetime"]) / 1e3))
            now = datetime.datetime.now()
            time_until = start_time - now
            minutes_until = divmod(time_until.total_seconds(), 60) # must do this because there is no minutes section
            print(minutes_until)
            #self.createMQID(match[1], start_time, c=cursor)
            if minutes_until[0] < 6 or time_until.days < 0:# and minutes_until[0] > 0:
                print("Updating : ", match[1])
                try:
                    if match[4] != 1:
                        self.createMTID(match[1], c=cursor, d=data)
                        cursor.execute("UPDATE matchqueue SET matchqueue.saved = 1 WHERE matchqueue.match_id = '" + match[1] + "'")
                        self.cnx.commit()
                        pass
                    else:
                        print("Already have match saved")

                except PlayerDataUnscrapableException:
                    print("player data was unscrapable for this match . . . . Deleting off Queue")
                    cursor.execute("DELETE FROM matchqueue WHERE matchqueue.match_id = '" + match[1] + "'")
                    self.cnx.commit()
                    continue
                print("######", data['live'])
                if data['live'] == False:
                    cursor.execute("UPDATE matchqueue SET matchqueue.started = 2 WHERE matchqueue.match_id = '" + match[1] + "'")
                    self.cnx.commit()
                elif data['live']:
                    cursor.execute("UPDATE matchqueue SET matchqueue.started = 1 WHERE matchqueue.match_id = '" + match[1] + "'")
                    self.cnx.commit()
            if minutes_until[0] >400:
                break

        #------------------Checking Online to Local--------------
        for match in matches_online:
            print(match)
            try:
                data = getMatchData(match)
            except MatchDataUnscrapableException:
                print("There is not enough data on this match yet")
                continue
            start_time = datetime.datetime.fromtimestamp((int(data["start_datetime"]) / 1e3))
            now = datetime.datetime.now()
            time_until = start_time - now
            minutes_until = divmod(time_until.total_seconds(), 60)
            if minutes_until[0] >400:
                break
            cursor.execute(
                "SELECT * FROM matchqueue WHERE matchqueue.match_id = '" + match +"'"
            )
            self.cnx.commit()
            if cursor.rowcount == 0:
                self.createMQID(match, start_time, c=cursor)

        print("`augury`.`matchqueue` has been updated")
        if c == None:
            cursor.close()

    def updateResults(self, c=None):

        if c == None:
            cursor = self.cnx.cursor()
        else:
            cursor = c

        cursor.execute("SELECT * FROM matchqueue WHERE matchqueue.started = 2")
        matches_local = cursor.fetchall()

        for match in matches_local:
            data = getResultMatchData(match[1])
            update_mtid = (
                    "UPDATE matches SET"
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
                    "WHERE matches.match_id = '" + match[1].strip() +"'")

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


            mtid_data = (
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
            print(len(mtid_data))


            cursor.execute(update_mtid, mtid_data)
            self.cnx.commit()

            cursor.execute("DELETE FROM matchqueue WHERE matchqueue.match_id = '" + match[1] + "'")
            self.cnx.commit()


        if c == None:
            cursor.close()
