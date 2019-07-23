import requests
from bs4 import BeautifulSoup
import traceback
from src.Exceptions import PlayerDataUnscrapableException
from src.Exceptions import MatchDataUnscrapableException
from src.Exceptions import MatchesListDataUnscrapableException
import time
from datetime import datetime, timedelta
from src.Logger import Logger

headers = requests.utils.default_headers()
li = Logger()


def getMatchOver(match_id):
    url='https://www.hltv.org' + match_id
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    countdown = soup.findAll('div', class_="countdown")[0].text.strip().lower()
    if countdown == "match over":
        return "MO"
    elif countdown == "live":
        return "LI"
    else:
        return "NL"

def getPlayerData(id,name):
    print("Scraper: getting player data for - ", id, "/", name)
    try:
        url='https://www.hltv.org/stats/players/'+str(id)+'/'+str(name)
        headers = requests.utils.default_headers()
        headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data = {row.findAll('div')[-1].text.strip() : row.findAll('div')[0].text.strip() for row in soup.findAll('div',class_='center-column row-item')}
        data['Teammate IDs'] = ",".join(','.join(x.find('a').get('href').split('/')[-2:]) for x in soup.findAll('div',class_='col teammate standard-box'))
        data.update({row.findAll('span')[0].text.strip() : row.findAll('span')[1].text.strip() for row in soup.find('div',class_='statistics').find('div',class_='columns').findAll('div',class_='stats-row')})
        url='https://www.hltv.org/stats/players/individual/'+str(id)+'/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({row.findAll('span')[0].text.strip() : row.findAll('span')[1].text.strip() for row in soup.find('div',class_='statistics').find('div',class_='columns').findAll('div',class_='stats-row')})
        url='https://www.hltv.org/stats/players/clutches/'+str(id)+'/1on1/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({"1 on 1 " + str(row.find('div',class_='description').text.strip()) : row.find('div',class_='value').text.strip() for row in soup.find('div',class_='summary').findAll('div',class_='col')})
        url='https://www.hltv.org/stats/players/clutches/'+str(id)+'/1on2/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({"1 on 2 " + str(soup.find('div',class_='summary').find('div',class_='col').find('div',class_='description').text.strip()) : soup.find('div',class_='summary').find('div',class_='col').find('div',class_='value').text.strip() })
        url='https://www.hltv.org/stats/players/clutches/'+str(id)+'/1on3/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({"1 on 3 " + str(soup.find('div',class_='summary').find('div',class_='col').find('div',class_='description').text.strip()) : soup.find('div',class_='summary').find('div',class_='col').find('div',class_='value').text.strip() })
        url='https://www.hltv.org/stats/players/clutches/'+str(id)+'/1on4/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({"1 on 4 " + str(soup.find('div',class_='summary').find('div',class_='col').find('div',class_='description').text.strip()) : soup.find('div',class_='summary').find('div',class_='col').find('div',class_='value').text.strip() })
        url='https://www.hltv.org/stats/players/clutches/'+str(id)+'/1on5/'+str(name)
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        data.update({"1 on 5 " + str(soup.find('div',class_='summary').find('div',class_='col').find('div',class_='description').text.strip()) : soup.find('div',class_='summary').find('div',class_='col').find('div',class_='value').text.strip() })

        #added by Chris
        url='https://www.hltv.org/player/'+str(id)+'/'+str(name)
        headers = requests.utils.default_headers()
        headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')

        data.update({"Rating 2.0" : str(soup.find('div', class_='two-col').find('div', class_='col').find('div', class_='cell').find('span', class_='statsVal').text.strip())})
        return data
    except Exception:
        print("Player scrping excpetion")
        raise PlayerDataUnscrapableException("Player Data Unscrapable")

def getMatches():
    try:
        url='https://www.hltv.org/matches'
        headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        #murls=['https://www.hltv.org' + x.get('href') for x in soup.find('div',class_='upcoming-matches').findAll('a')]
        m=[x.get('href') for x in soup.find('div',class_='upcoming-matches').findAll('a')]
        return m
    except Exception:
        raise MatchesListDataUnscrapableException("Matches Data Unscrapable")

def getMatchData(match_id):
    print("Scraper.py: getting Match data for ", match_id)
    try:
        url = 'https://www.hltv.org' + match_id
        headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
        soup=BeautifulSoup(requests.get(url,headers=headers).content,'html.parser')
        t1url='https://www.hltv.org' + soup.find('div',class_='standard-box teamsBox').findAll('div',class_='team')[0].find('a').get('href')
        t2url='https://www.hltv.org' + soup.find('div',class_='standard-box teamsBox').findAll('div',class_='team')[-1].find('a').get('href')
        soup1=BeautifulSoup(requests.get(t1url,headers=headers).content,'html.parser')
        soup2=BeautifulSoup(requests.get(t2url,headers=headers).content,'html.parser')
        live = False
        try:
            if soup.find('div', class_='countdown').text.strip() == "LIVE":
                live = True
        except Exception:
            live = False
        return { "match_id": match_id , "team_1" : {"team_id" : '/'.join(t1url.split('/')[-2:]) , "players" : ['/'.join(x.get('href').split('/')[-2:]) for x in soup1.find('div',class_='bodyshot-team-bg').findAll('a')] , "team_country" : soup1.find('div',class_='team-country').text.strip()}, "team_2" : {"team_id" : '/'.join(t2url.split('/')[-2:]) , "players" : ['/'.join(x.get('href').split('/')[-2:]) for x in soup2.find('div',class_='bodyshot-team-bg').findAll('a')] , "team_country" : soup2.find('div',class_='team-country').text.strip()}, "start_datetime" : soup.find('div',class_='timeAndEvent').find('div',class_='time').get('data-unix'), "match_type": soup.find('div', class_='standard-box veto-box').find('div', class_='padding preformatted-text').text.strip(), "live":live}
    except Exception:
        raise MatchDataUnscrapableException("Match Data Unscrapable")

def getUpcomingMatches(interval_minutes):
    url='https://www.hltv.org/matches'
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    data = []
    murls=[( x.get('href'), datetime.fromtimestamp(int(x.find('div', class_='time').get('data-unix'))/1000)) for x in soup.find('div',class_='upcoming-matches').findAll('a')]
    now = datetime.now()
    until_match_limit = now + timedelta(days=0, minutes = interval_minutes)
    ret_urls = []
    for i in range(len(murls)):
        try:
            url = murls[i][0]
            start_time = murls[i][1]
        except IndexError:
            break
        if start_time < until_match_limit:
            ret_urls.append(murls[i])
    return(ret_urls)

def get50MatchData(): #not error handled
    url='https://www.hltv.org/matches'
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    data={}
    murls=['https://www.hltv.org' + x.get('href') for x in soup.find('div',class_='upcoming-matches').findAll('a')]
    counter=1
    for url in murls:
        try:
            print('Scraping match {0} of {1}'.format(counter,len(murls)))
            soup=BeautifulSoup(requests.get(url,headers=headers).content,'html.parser')
            t1url='https://www.hltv.org' + soup.find('div',class_='standard-box teamsBox').findAll('div',class_='team')[0].find('a').get('href')
            t2url='https://www.hltv.org' + soup.find('div',class_='standard-box teamsBox').findAll('div',class_='team')[-1].find('a').get('href')
            soup1=BeautifulSoup(requests.get(t1url,headers=headers).content,'html.parser')
            soup2=BeautifulSoup(requests.get(t2url,headers=headers).content,'html.parser')
            data['match_' + str(counter) + '_id'] = { '/'.join(url.split('/')[-2:]) : { "team_1" : {"team_id" : '/'.join(t1url.split('/')[-2:]) , "players" : ['/'.join(x.get('href').split('/')[-2:]) for x in soup1.find('div',class_='bodyshot-team-bg').findAll('a')] , "team_country" : soup1.find('div',class_='team-country').text.strip()}, "team_2" : {"team_id" : '/'.join(t2url.split('/')[-2:]) , "players" : ['/'.join(x.get('href').split('/')[-2:]) for x in soup2.find('div',class_='bodyshot-team-bg').findAll('a')] , "team_country" : soup2.find('div',class_='team-country').text.strip()}}, "start_datetime" : soup.find('div',class_='timeAndEvent').find('div',class_='time').get('data-unix')}
            counter+=1
        except Exception as e:
            print(e)
            continue
    return data

def getResultMatchData(match_id):
    matchurl = "https://www.hltv.org" + match_id
    print(matchurl)
    print('\033[1;37;40mSetting Headers' ,end=' ')
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    print('\033[1;32;40mDone')
    print('\033[1;37;40mScraping page' ,end=' ')
    page=''
    while 'Response' not in str(page):
        try:
            page=requests.get(matchurl,headers=headers)
        except:
            print("\033[1;31;40mSomething went wrong, attempting again in 10 seconds")
            time.sleep(10)
            pass
    print('\033[1;32;40mDone')
    soup=BeautifulSoup(page.content,'html.parser')
    print('\033[1;37;40mExtracting Data' ,end=' ')
    data=''
    data={'match_id' : '/'+'/'.join(matchurl.split('/')[3:])}
    t1_overall_score=''
    try:
        t1_overall_score=soup.find('div',class_='standard-box teamsBox').find('div',class_='team1-gradient').findAll('div')[-1].text
    except:
        t1_overall_score=''
        t2_overall_score=''
    try:
        t2_overall_score=soup.find('div',class_='standard-box teamsBox').find('div',class_='team2-gradient').findAll('div')[-1].text
    except:
        t2_overall_score=''
        t1_win='Draw'
        t1_win=int(t1_overall_score) > int(t2_overall_score)

        data['t1_overall_score'] = t1_overall_score
        data['t2_overall_score'] = t2_overall_score
        data['t1_win'] = t1_win

        no_of_maps=''
    try:
        no_of_maps=len(soup.find('div',class_='flexbox-column').findAll('div',class_='mapholder'))
    except:
        no_of_maps=''

    mapdata=[]

    for x in range(no_of_maps):
        mapname=''
        try:
          mapname=soup.find('div',class_='flexbox-column').findAll('div',class_='mapholder')[x].find('div',class_='mapname').text
        except:
          mapname=''
          map_score=''
        try:
          map_score=''.join(x.text for x in soup.find('div',class_='flexbox-column').findAll('div',class_='mapholder')[x].find('div',class_='results').findAll('span')[:3])
          t1_map1_score=map_score.split(':')[0]
          t2_map1_score=map_score.split(':')[-1]
          t1_map1_win='Draw'
          t1_map1_win=int(t1_map1_score) > int(t2_map1_score)
        except:
          map_score=''
          t1_map1_score=None
          t2_map1_score=None
          t1_map1_win=None
        mapdata.append([mapname,t1_map1_score,t2_map1_score,t1_map1_win])

    for x in range(len(mapdata)):
        if x==5:
          break
        data['map' + str(x+1)] = mapdata[x][0]
        data['t1_map' + str(x+1) + '_score'] = mapdata[x][1]
        data['t2_map' + str(x+1) + '_score'] = mapdata[x][2]
        data['t1_map' + str(x+1) + '_win'] = mapdata[x][3]
        print('\033[1;32;40mDone\033[1;37;40m')

    return data
