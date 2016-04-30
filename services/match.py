from listeners import StdCommandListener
import requests
import datetime
import json

class EchoListener(StdCommandListener):
    def __init__(self):
        super().__init__("match")

    def onCommand(self, bot, message, args):
        with open('api_key.json') as f:
            data = json.load(f)
        api_key = data['key']
        match_id = args[0]
        match_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id={}&key={}".format(match_id, api_key)
        hero_url = "http://api.steampowered.com/IEconDOTA2_205790/GetHeroes/v0001/?language=en&key={}".format(api_key)
        r_hero = requests.get(hero_url)
        r_hero_json = r_hero.json()
        r = requests.get(match_url)
        r_json = r.json()
        if r_json['result']['radiant_win'] == 'True':
            winner = "Radiant"
        else:
            winner = "Dire"
        duration = r_json['result']['duration']
        bot.respond(message, 'Match {} | {} Victory | Match Duration: {}'.format(match_id, winner, str(datetime.timedelta(seconds=duration))))
        player_id = []
        hero_id = []
        gold_id = []
        kda_id = []
        cs_id = []
        xpm_id = []
        gpm_id = []
        hdhh_id = []
        td_id = []
        for x in range(0, 10):
            if r_json['result']['players'][x]['account_id'] == 4294967295:
                player_id.append("Anonymous")
            elif r_json['result']['players'][x]['account_id'] != 4294967295:
                temp_player_id = r_json['result']['players'][x]['account_id'] + 76561197960265728
                player_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(api_key, temp_player_id)
                r2 = requests.get(player_url)
                r2_json = r2.json()
                player_id.append(r2_json['response']['players'][0]['personaname'])
            for y in range(0, 111):
                if r_hero_json['result']['heroes'][y]['id'] == r_json['result']['players'][x]['hero_id']:
                    hero_id.append(r_hero_json['result']['heroes'][y]['localized_name'])
            gold_id.append(r_json['result']['players'][x]['gold'])
            kills = r_json['result']['players'][x]['kills']
            deaths = r_json['result']['players'][x]['deaths']
            assists = r_json['result']['players'][x]['assists']
            kda_id.append("{}/{}/{}".format(kills, deaths, assists))
            cs = r_json['result']['players'][x]['last_hits']
            dn = r_json['result']['players'][x]['denies']
            cs_id.append("{}/{}".format(cs,dn))
            xpm_id.append(r_json['result']['players'][x]['xp_per_min'])
            gpm_id.append(r_json['result']['players'][x]['gold_per_min'])
            hd = r_json['result']['players'][x]['hero_damage']
            hh = r_json['result']['players'][x]['hero_healing']
            hdhh_id.append("{}/{}".format(hd, hh))
            td_id.append(r_json['result']['players'][x]['tower_damage'])

        bot.respond(message, "Team Radiant:")
        for x in range(0, 5):
            bot.respond(message, "{}({})|KDA:{}|LH/DN:{}|Gold:{}|XPM:{}|GPM:{}|HD/HH:{}|TD:{}".format(player_id[x], hero_id[x], kda_id[x], cs_id[x], gold_id[x], xpm_id[x], gpm_id[x], hdhh_id[x], td_id[x]))
        bot.respond(message, "Team Dire:")
        for x in range(5, 10):
            bot.respond(message, "{}({})|KDA:{}|LH/DN:{}|Gold:{}|XPM:{}|GPM:{}|HD/HH:{}|TD:{}".format(player_id[x], hero_id[x], kda_id[x], cs_id[x], gold_id[x], xpm_id[x], gpm_id[x], hdhh_id[x], td_id[x]))


