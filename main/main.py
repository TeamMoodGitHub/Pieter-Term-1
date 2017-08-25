from flask import Flask, request, render_template
import requests

champions = []
for i in range(0,500):
	champions.append("Error")
champions[7] = "LeBlanc"
champions[9] = "Fiddlesticks"
champions[15] = "Sivir"
champions[16] = "Soraka"
champions[18] = "Tristana"
champions[19] = "Warwick"
champions[22] = "Ashe"
champions[24] = "Jax"
champions[29] = "Twitch"
champions[35] = "Shaco"
champions[42] = "Corki"
champions[55] = "Katarina"
champions[62] = "Wukong"
champions[76] = "Nidalee"
champions[78] = "Poppy"
champions[80] = "Pantheon"
champions[99] = "Lux"
champions[103] = "Ahri"
champions[104] = "Graves"
champions[112] = "Viktor"
champions[114] = "Fiora"
champions[122] = "Darius"
champions[143] = "Zyra"
champions[202] = "Jhin"
champions[222] = "Jinx"
champions[240] = "Kled"
champions[254] = "Vi"
champions[498] = "Xayah"

app = Flask(__name__)

def get_id(base,username,key):
	url = base + "summoner/v3/summoners/by-name/" + username + "?" + key
	response = requests.get(url)
	return response.json()
	
def get_matchlist(base,accountID,key):
	url = base + "match/v3/matchlists/by-account/" + accountID + "/recent/?" + key
	response = requests.get(url)
	return response.json()
	
def get_matchdata(base,gameID,accountID,regionID,key):
	url = base + "match/v3/matches/" + gameID + "?forAccountId=" + accountID + "&forPlatformId=" + regionID + "&" + key
	response = requests.get(url)
	return response.json()
		
	#def get_champion(base,championID,end):
#	url = base + "static-data/v3/champions/" + championID + end
#	response = requests.get(url)
#	return response.json()


@app.route('/')
def home():
    return render_template("input.html")
	
@app.route('/', methods=['POST'])
def basics():
	username = request.form['username']
	region = request.form['region']
	key = request.form['key']
	if region == "EUW":
		regionID = "euw1"
	else:
		regionID = "na1"
	base = "https://" + regionID + ".api.riotgames.com/lol/"
	key = "api_key=" + key
	idJSON = get_id(base,username,key)
	ID = str(idJSON['id'])
	accountID = str(idJSON['accountId'])
	matchlistJSON = get_matchlist(base,accountID,key)
	gameID = []
	championID = []
	champion = []
	duration_s = []
	duration_t = []
	result = []
	kills = []
	deaths = []
	assists = []
	CS = []
	color = []
	#KDA = []	
	for i in range(0,20):
		gameID.append(str(matchlistJSON['matches'][i]['gameId']))
		championID.append(matchlistJSON['matches'][i]['champion'])
		champion.append(champions[championID[i]])
		matchJSON = get_matchdata(base,gameID[i],accountID,regionID,key)
		duration_s.append(matchJSON['gameDuration'])
		m, s = divmod(duration_s[i],60)
		h, m = divmod(m, 60)
		h = str(h)
		if m < 10:
			m = str(m)
			m = '0' + m
		else:
			m = str(m)
		if s < 10:
			s = str(s)
			s = '0' + s
		else:
			s = str(s)
		duration_t.append(h + ":" + m + ":" + s)
		for j in range(0,10):
			if str(matchJSON['participantIdentities'][j]['player']['summonerId']) == ID:
				participantID = j+1
				break
		result.append(str(matchJSON['participants'][participantID-1]['stats']['win']))
		if result[i] == "True":
			color.append("LimeGreen")
		else:
			color.append("LightCoral")
		kills.append(str(matchJSON['participants'][participantID-1]['stats']['kills']))
		deaths.append(str(matchJSON['participants'][participantID-1]['stats']['deaths']))
		assists.append(str(matchJSON['participants'][participantID-1]['stats']['assists']))
		CS.append(str(matchJSON['participants'][participantID-1]['stats']['totalMinionsKilled']))
		#KDA.append((kills + "/" + deaths + "/" + assists))
	return render_template("main.html",username=username, champion=champion, kills=kills,	\
		deaths=deaths, assists=assists, CS=CS, duration=duration_t, color=color)

#For later:
#@app.route('/details')		
#def details():	

	
if __name__ == "__main__":
    app.run()
