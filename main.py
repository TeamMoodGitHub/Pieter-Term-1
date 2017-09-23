from flask import Flask, request, render_template, url_for
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import requests, pickle
import base64
#pillow

champions = []
for i in range(0,517):
	champions.append("Error")
champions[7] = "LeBlanc"; champions[9] = "Fiddlesticks"; champions[15] = "Sivir"; champions[16] = "Soraka"
champions[18] = "Tristana"; champions[19] = "Warwick"; champions[22] = "Ashe"; champions[24] = "Jax"
champions[11] = "Master Yi"; champions[29] = "Twitch"; champions[35] = "Shaco"; champions[42] = "Corki"
champions[55] = "Katarina"; champions[62] = "Wukong"; champions[76] = "Nidalee"; champions[78] = "Poppy"
champions[80] = "Pantheon"; champions[99] = "Lux"; champions[103] = "Ahri"; champions[104] = "Graves"
champions[112] = "Viktor"; champions[114] = "Fiora"; champions[122] = "Darius"; champions[143] = "Zyra"
champions[202] = "Jhin"; champions[222] = "Jinx"; champions[240] = "Kled"; champions[254] = "Vi"
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
	
def get_timeline(base,gameID,key):
	url = base + "match/v3/timelines/by-match/" + gameID + "?" + key
	response = requests.get(url)
	return response.json()
	
	

#def get_champions():
#	url = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
#	response = requests.get(url)
#	return response.json()
		
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
	#static_base = "http://ddragon.leagueoflegends.com/"
	idJSON = get_id(base,username,key)
	ID = str(idJSON['id'])
	accountID = str(idJSON['accountId'])
	try:
		matchlistJSON = get_matchlist(base,accountID,key)
	except KeyError:
		return render_template("error.html",username=username)
	#championJSON = get_champions()
	gameID = []; championID = []; champion = []; duration_s = []
	duration_t = []; result = []; kills = []; deaths = []
	assists = []; CS = []; color = []; mode = [];
	for i in range(0,20):
		gameID.append(str(matchlistJSON['matches'][i]['gameId']))
		championID.append(matchlistJSON['matches'][i]['champion'])
		champion.append(champions[championID[i]])
		#for j in range(0,140):
		#	if str(matchJSON['data'][])
		#champion.append(str(championJSON['data']))
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
		mode.append(matchJSON['gameMode'])
		#KDA.append((kills + "/" + deaths + "/" + assists))
	with open('data.pickle', 'wb') as f:
		for var in [base, key, regionID, accountID, ID, gameID, champion]:
			pickle.dump(var, f, pickle.HIGHEST_PROTOCOL)
	return render_template("main.html",username=username, champion=champion, kills=kills,	\
		deaths=deaths, assists=assists, CS=CS, duration=duration_t, color=color, mode=mode)
		
@app.route('/detail<game>')		
def details(game):
	plt.clf()
	plt.close("all")
	with open('data.pickle', 'rb') as f:
		base = pickle.load(f)
		key = pickle.load(f)
		regionID = pickle.load(f)
		accountID = pickle.load(f)
		ID = pickle.load(f)
		gameID = pickle.load(f)
		champion = pickle.load(f)
	matchJSON = get_matchdata(base,gameID[int(game)-1],accountID,regionID,key)
	duration_s = matchJSON['gameDuration']
	m, s = divmod(duration_s,60)
	for j in range(0,10):
		if str(matchJSON['participantIdentities'][j]['player']['summonerId']) == ID:
			participantID = j+1
			break
	timelineJSON = get_timeline(base,gameID[int(game)-1],key)
	dframe = timelineJSON['frameInterval']
	CSdata = []; CSperminute = []; CSgoal = []
	time = []; deaths = []; kills = []; check = 0
	xPosKill = []; yPosKill = []
	xPosDeath = []; yPosDeath = []
	for i in range(0,m+1):
		j = 0
		CSdata.append(timelineJSON['frames'][i]['participantFrames'][str(participantID)]['minionsKilled'])
		time.append(i)
		CSgoal.append(i*8)
		if i == 0:
			CSperminute.append(0)
		else:
			CSperminute.append(CSdata[i]-CSdata[i-1])
		while True:
			try:
				type = str(timelineJSON['frames'][i]['events'][j]['type'])
				if type == 'CHAMPION_KILL':
					if timelineJSON['frames'][i]['events'][j]['victimId'] == participantID:
						deaths.append(timelineJSON['frames'][i]['events'][j]['timestamp'])
						xPosDeath.append(timelineJSON['frames'][i]['events'][j]['position']['x'])
						yPosDeath.append(timelineJSON['frames'][i]['events'][j]['position']['y'])
					elif timelineJSON['frames'][i]['events'][j]['killerId'] == participantID:
						kills.append(timelineJSON['frames'][i]['events'][j]['timestamp'])
						xPosKill.append(timelineJSON['frames'][i]['events'][j]['position']['x'])
						yPosKill.append(timelineJSON['frames'][i]['events'][j]['position']['y'])
				j += 1
			except IndexError:
				break
		if champion[int(game)-1] == 'Viktor' and check == 0:
			j = 0
			while True:
				try:
					type = str(timelineJSON['frames'][i]['events'][j]['type'])
					if type == 'ITEM_PURCHASED':
						if timelineJSON['frames'][i]['events'][j]['participantId'] == participantID and	timelineJSON['frames'][i]['events'][j]['itemId'] == 3196:
							upgrade = timelineJSON['frames'][i]['events'][j]['timestamp']
							check = 1
							break
					j += 1
				except IndexError:
					break
	plt.plot(time, CSdata, label="Your CS")
	plt.plot(time, CSgoal, label="8 CS per minute")
	if len(deaths) != 0:
		deaths = np.divide(deaths,dframe)
		for i in range(0,len(deaths)):
			if i == 0:
				plt.axvline(deaths[i], ymin=0, ymax=1, color='red', label='Deaths')
			else:
				plt.axvline(deaths[i], ymin=0, ymax=1, color='red')
	if len(kills) != 0:
		kills = np.divide(kills,dframe)
		for i in range(0,len(kills)):
			if i == 0:
				plt.axvline(kills[i], ymin=0, ymax=1, color='black', label='Kills')
			else:
				plt.axvline(kills[i], ymin=0, ymax=1, color='black')
	if 'upgrade' in locals():
		upgrade = np.divide(upgrade,dframe)
		plt.axvline(upgrade, ymin=0, ymax=1, color='green', label='Hex Core mk-1 Upgrade')
	plt.legend(loc='upper left')
	plt.ylabel('CS (only minions)')
	plt.xlabel('Gametime [min]')
	img = BytesIO()
	plt.savefig(img, format='png')
	img.seek(0)
	plot_url = base64.b64encode(img.getvalue()).decode('ascii')
	plt.close()
	plt.bar(time, CSperminute, 0.8, color='blue', label="Your CS")
	plt.legend(loc='upper left')
	plt.ylabel('CS per minute (only minions)')
	plt.xlabel('Gametime [min]')
	img = BytesIO()
	plt.savefig(img, format='png')
	img.seek(0)
	plot_url2 = base64.b64encode(img.getvalue()).decode('ascii')
	plt.close()
	img = plt.imread("static/map.PNG")
	fig, ax = plt.subplots()
	plt.scatter(xPosDeath, yPosDeath, color='red', label="Death")
	plt.scatter(xPosKill, yPosKill, color='black', label="Kill")
	if participantID < 6:
		plt.scatter(600,600,s=100,color='cyan')
	else:
		plt.scatter(14220,14281,s=100,color='tomato')
	plt.legend(loc='upper left')
	ax.imshow(img, extent=[0,14820,0,14881])
	plt.xlim([0,14820])
	plt.ylim([0,14881])
	plt.axis('off')
	img = BytesIO()
	plt.savefig(img, format='png')
	img.seek(0)
	plot_url3 = base64.b64encode(img.getvalue()).decode('ascii')
	return render_template("details.html", plot_url=plot_url, plot_url2=plot_url2, plot_url3=plot_url3)

	
if __name__ == "__main__":
    app.run()
