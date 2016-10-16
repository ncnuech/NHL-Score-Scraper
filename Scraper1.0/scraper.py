#!/usr/bin/python3
from lxml import html
import requests

import os
import signal
import time

import threading
import subprocess
import time
import datetime

import logging

import smtplib

import calendar

class Messenger:
	webPrefixAction="http://noahn.me/getPhoneForActions?type="
	webPrefixPlayerOfDay="http://noahn.me/getPhoneForPlayerOfDay"
	def __init__(self):
		return
	def sendMessage(self,message,type):
		phoneListStr=""
		phoneListStr = requests.get(self.webPrefixAction + type)
		phoneList = phoneListStr.text.split(' ')
		message=message[len(printerObj.prefix)+4:]
		messageList=message.split('~')
		finalMessage=""
		for msg in messageList:
			msg=msg[8:]
			finalMessage+=msg
		print(finalMessage)
		print(len(finalMessage))
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login('noahnuechterlein@gmail.com','Felipe12')
		for phone in phoneList:
			server.sendmail('noahnuechterlein@gmail.com',phone+'@vtext.com',finalMessage)
		server.quit()


class Printer:
	lastPrintWasSummary=False

	#prefix="http://10.177.105.74:81/text/"
	prefix="http://10.177.105.138/arduino/text/"
	webPrefix="http://noahn.me/getMessage?message="
	brightness="30"

	#Color Then 0-9
	def __init__(self):
		return

	def printToBoard(self,outStr,type):
		print("\n")
		#outStr=outStr[:150]
		if ESPNSportsObj.gamesOver==True:
			rval = requests.get("")
			return;
		if (type=="Summary" and len(outStr) == 1):
			if self.lastPrintWasSummary==True:
				return
			self.lastPrintWasSummary=True
		else:
			self.lastPrintWasSummary=False
		#while check if done is false, wait some 
		for strComponent in outStr:
			strComponent=self.prefix+strComponent
			print(strComponent)
			rval = requests.get(strComponent)#uncomment
			rval2 = requests.get(self.webPrefix+outStr[0])
			if (type=="action"):
				messengerObj.sendMessage(strComponent,type)
			time.sleep(15)
		print("\n")
	def printTest(self,outStr):
		rval = requests.get(self.prefix+outStr)
		return


	def debugPrint(self,outStr):
		print("\tdebug:\t"+outStr)


#Class Describing data for an individual game
#Used to retrieve game data and check for score changes
class Game:

	#Name of Away Team
	awayTeam = ""
	#Name of Home Team
	homeTeam = ""
	#Score of Away Team
	awayScore = 0
	#Score of Home Team
	homeScore = 0

	#url to find details about the game including previous scoring play
	url = ""
	#Boolean for whether game has started True if started (unimplemented)
	gameStarted = False;
	#Boolean for whether game has ended True if ended (unimplemented)
	gameEnded = False;
	#string for type of game status used for end game right now
	gameStatusStr = "";

	gameTime=""
	numTimesChecked=0
	#id used to identify a given game(most notibly used by ESPN.com)
	gameId = 0;

	#Constructor for a game, called once as "Game()"
	#_awayTeam --- name of away team
	#_homeTeam --- name of home team
	#_url --- url for further game details
	def __init__(self,_awayTeam,_homeTeam,_url):
		printerObj.debugPrint("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url

	def __init__(self,_awayTeam,_homeTeam,_url,_gameId):
		printerObj.debugPrint("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url
		self.gameId = _gameId

	#checks current score of game(passed in) with previously documented values
	#returns true if score has changed, else returns false
	#newAwayScore --- newest away team score to compare
	#newHomeScore --- newest home team score to compare
	def checkScore(self,newAwayScore,newHomeScore):
		changed=0
		if(newAwayScore != self.awayScore):
			self.awayScore = newAwayScore
			changed=1
			
		if (newHomeScore != self.homeScore):
			self.homeScore = newHomeScore
			changed=2
			
		return changed
	
	def getScoringTeamName(self,scoringTeam):
		if (scoringTeam==1):
			return self.awayTeam
		return self.homeTeam

class League:

	teamDict = {}

	def setupTeamDict(self):

		prefix = "BuzzerSounds/"
		self.teamDict["Blackhawks"] = {"abbr":"CHI","buzzerFile":prefix+ "chicago.mp3","hex":"~480000"}
		self.teamDict["Avalanche"] = {"abbr":"COL","buzzerFile":prefix + "colorado.mp3","hex":"~830018"}
		self.teamDict["Stars"] = {"abbr":"DAL","buzzerFile": prefix + "dallas.mp3","hex":"~084c00"}
		self.teamDict["Wild"] ={"abbr":"MIN","buzzerFile":prefix + "minnesota.mp3","hex":"~103d17"}
		self.teamDict["Predators"] = {"abbr":"NSH","buzzerFile":prefix + "nashville.mp3","hex":"~ffb71a"}
		self.teamDict["Blues"] = {"abbr":"STL","buzzerFile":prefix + "stlouis.mp3","hex":"~083377"}
		self.teamDict["Jets"] = {"abbr":"WIN","buzzerFile":prefix + "winnepeg.mp3","hex":"~002e62"}
		self.teamDict["Bruins"] = {"abbr":"BOS","buzzerFile":prefix+"boston.mp3","hex":"~fcb930"}
		self.teamDict["Sabres"] = {"abbr":"BUF","buzzerFile":prefix+"buffalo.mp3","hex":"~9e4e00"}
		self.teamDict["Red Wings"] = {"abbr":"DET","buzzerFile":prefix+ "detroit.mp3","hex":"~ff0000"}
		self.teamDict["Panthers"] = {"abbr":"FLA","buzzerFile":prefix+"florida.mp3","hex":"~c49818"}
		self.teamDict["Canadiens"] = {"abbr":"MTL","buzzerFile":prefix+"montreal.mp3","hex":"~ff0000"}
		self.teamDict["Senators"] = {"abbr":"OTT","buzzerFile":prefix+"ottawa.mp3","hex":"~D47E00"}
		self.teamDict["Lightning"] = {"abbr":"TB","buzzerFile":prefix+"tampabay.mp3","hex":"~ffffff"}
		self.teamDict["Maple Leafs"] = {"abbr":"TOR","buzzerFile":prefix+"toronto.mp3","hex":"~013e7f"}
		self.teamDict["Ducks"] = {"abbr":"ANA","buzzerFile":prefix+"anaheim.mp3","hex":"~c2672c"}
		self.teamDict["Coyotes"] = {"abbr":"ARI","buzzerFile":prefix+ "arizona.mp3","hex":"~3d0100"}
		self.teamDict["Flames"] = {"abbr":"CGY","buzzerFile":prefix+ "calgary.mp3","hex":"~c90000"}
		self.teamDict["Oilers"] = {"abbr":"EDM","buzzerFile":prefix+ "edmonton.mp3","hex":"~eb6e1e"}
		self.teamDict["Kings"] = {"abbr":"LA","buzzerFile":prefix+"losangeles.mp3","hex":"~231f20"}
		self.teamDict["Sharks"] = {"abbr":"SJ","buzzerFile":prefix+"sanjose.mp3","hex":"~00765D"}
		self.teamDict["Canucks"] = {"abbr":"VAN","buzzerFile":prefix+"vancouver.mp3","hex":"~013e7f"}
		self.teamDict["Hurricanes"] = {"abbr":"CAR","buzzerFile":prefix+"carolina.mp3","hex":"~ff0000"}
		self.teamDict["Blue Jackets"] = {"abbr":"CLS","buzzerFile":prefix+"columbus.mp3","hex":"~002e62"}
		self.teamDict["Devils"] = {"abbr":"NJ","buzzerFile":prefix+"newjersey.mp3","hex":"~ff0000"}
		self.teamDict["Islanders"] = {"abbr":"NYI","buzzerFile":prefix+"newyorkislanders.mp3","hex":"~ff5000"}
		self.teamDict["Rangers"] = {"abbr":"NYR","buzzerFile":prefix+"newyorkrangers.mp3","hex":"~005dab"}
		self.teamDict["Flyers"] = {"abbr":"PHI","buzzerFile":prefix+"philadelphia.mp3","hex":"~F32B00"}
		self.teamDict["Penguins"] = {"abbr":"PIT","buzzerFile":prefix+"pittsburgh.mp3","hex":"~7ed5fa"}
		self.teamDict["Capitals"] = {"abbr":"WSH","buzzerFile":prefix+"washington.mp3","hex":"~ff0000"}
		self.teamDict["Default"] = {"abbr":"DEF","buzzerFile":prefix+"gameOver.mp3","hex":"~ffffe6"}


	def getFormattedTeamString(self,teamName):
		defaultBrightness="30"
		return self.teamDict[teamName]['hex'] + defaultBrightness + self.teamDict[teamName]['abbr'] + self.teamDict['Default']['hex'] + defaultBrightness

	def getAllTeamsStr(self):
		leagueStr = ""
		for team in self.teamDict:
			teamStr = self.teamDict[team]['hex'] + "30"+ self.teamDict[team]['abbr']
			leagueStr = leagueStr + teamStr + " "
		print(leagueStr)
		leagueArray=[]
		leagueArray.append(leagueStr)
		printerObj.printToBoard(leagueArray,"test")
		return 
	def __init__(self):
		self.setupTeamDict()
###############################################
#Code to play sound (unfinished)
#threading starts a 2nd thread in a callback function
#code is using vlc in specific location on device
#call subprocess with vlc then shut down after x seconds
class Buzzer:

	#starts the buzzer when a specific team scores. must call with team name
	#uses vlc player right now. will have to work if go to rPI
	#currently 10 seconds to end buzzer
	#buzzers will play on top of each other
	def startBuzzer(self,teamName):
		time.sleep(10)

		playTime=10
		if (teamName=="Default"):
			playTime=8
		if os.name=="nt":
			sound_player = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
		else:
			sound_player = "/usr/bin/cvlc"
		sound_file = leagueObj.teamDict[teamName]['buzzerFile']
		print("file" + sound_file)
		music_player_subprocess = subprocess.Popen([sound_player,sound_file])
		threading.Timer(10.0,self.endBuzzer,[music_player_subprocess]).start()

	#call to end buzzer
	def endBuzzer(self,music_player_subprocess):
		os.kill(music_player_subprocess.pid, signal.SIGINT)

	def __init__(self):		
		return
###############################################
#no access to power play points
class Player:
	skater = False
	goalie = False
	name=""
	goals = 0
	assists = 0
	plusminus = 0
	pim = 0
	sog = 0
	wins = 0
	saveper = 0.0
	gaa = 0.0
	so = 0
	score=0
	url=""
	def setSkater(self,_name,_goals,_assists,_plusminus,_pim,_sog,_url):
		self.name=_name
		self.goals=_goals
		self.assists=_assists
		self.plusminus=_plusminus
		self.pim=_pim
		self.sog=_sog
		self.skater=True
		self.url=_url
		self.score = 1*self.goals+.75*float(self.assists)+.25*float(self.plusminus)+.15*float(self.pim)+.2*float(self.sog)
		return
	def setGoalie(self,_name,_wins,_saveper,_gaa,_so,_url):
		self.name=_name
		self.wins=_wins
		self.saveper=_saveper
		self.gaa=_gaa
		self.so=_so
		self.goalie=True
		self.url=_url
		self.score=self.wins*1.0+(3-self.gaa)+self.so*1.0+self.saveper*1
		return
	def __init__(self):		
		return

class ESPNSportsObj:

	#List of Game Objects that hold  data on games on the current day
	#Current day is currently Hardcoded
	#TODO grab game on current date
	gameList = []
	gamesOver = False
	gameOverCount=0
	playerList = []
	def __init__(self):
		self.startDay()
	def loadGamePlayers(self,game):
		time.sleep(.25);
		printerObj.debugPrint("get request to " + game.url)
		page = requests.get(game.url)
		tree = html.fromstring(page.content);

		playerStats =  tree.xpath('//*[@id="my-players-table"]/*/div[2]/table/thead/tr/td/*/div/table/tbody[1]/*');
		for player in playerStats:
			if not player.xpath('td[1]/a/text()') or not player.xpath('td[9]/text()'):
				continue;
			url = player.xpath('td[1]/a/@href')[0]
			name = player.xpath('td[1]/a/text()')[0]
			goals = int(player.xpath('td[2]/text()')[0])
			assists = int(player.xpath('td[3]/text()')[0])
			plusminus = int(player.xpath('td[4]/text()')[0])
			sog = int(player.xpath('td[5]/text()')[0])
			pim = int(player.xpath('td[9]/text()')[0])
			playerObj = Player()
			playerObj.setSkater(name,goals,assists,plusminus,pim,sog,url)
			self.playerList.append(playerObj)

		playerStats =  tree.xpath('//*[@id="my-players-table"]/div[6]/div[2]/table/thead/tr/*/div/div/table/tbody/*')
		first=True
		for player in playerStats:
			if not player.xpath('td[1]/a/text()'):
				continue;
			name = player.xpath('td[1]/a/text()')[0]
			url = player.xpath('td[1]/a/@href')[0]
			goalsAllowed=int(player.xpath('td[3]/text()')[0])
			saveper=float(player.xpath('td[5]/text()')[0])
			toi=player.xpath('td[6]/text()')[0]
			minutes=int(toi.split(':')[0])
			seconds=float(toi.split(':')[1])
			seconds=seconds/60.0
			amountofgame=(minutes+seconds)/60
			gaa=goalsAllowed/amountofgame
			if first:
				if game.awayScore>game.homeScore:
					wins=1
				else:
					wins=0
				first = False
			else:
				if game.homeScore>game.awayScore:
					wins=1
				else:
					wins=0
			if goalsAllowed==0:
				so=1
			else:
				so=0
			playerObj = Player()
			playerObj.setGoalie(name,wins,saveper,gaa,so,url)
			playerObj.score=playerObj.score*amountofgame
			self.playerList.append(playerObj)
		return

	def loadTopPlayerData(self,url):
		time.sleep(.5);
		printerObj.debugPrint("get request to " + url)
		page = requests.get(url)
		tree = html.fromstring(page.content);
		imgurl =  tree.xpath('//*[@id="content"]/div[3]/div[2]/div[2]/img/@src')[0];
		name = tree.xpath('//*[@id="content"]/div[3]/div[2]/h1/text()')[0];
		#color = tree.xpath('//*[@id="content"]/div[3]/div[2]/div[4]/table/thead/tr/th[3]');
		date = "Friday October 14th"

		month = time.strftime("%m") #oes this work for single digit days?
		day = time.strftime("%d") #oes this work for single digit days?
		year = time.strftime("%Y")
		numMonth=int(month)
		curTime = time.strftime("%H")
		if int(curTime)<7:
			yesterday = datetime.date.today() - datetime.timedelta(1)
			month=yesterday.strftime('%m')
			day=yesterday.strftime('%d')
		month = calendar.month_name[int(month)]
		ans = datetime.date(int(year), int(numMonth), int(day))
		dayOfWeek = ans.strftime("%A")
		if 4 <= int(day) <= 20 or 24 <= int(day) <= 30:
			suffix = "th"
		else:
			suffix = ["st", "nd", "rd"][int(day) % 10 - 1]
		date = dayOfWeek + " " + month + " " + day + suffix
		return date,name,imgurl

	def loadDayPlayers(self):
		for game in self.gameList:
			self.loadGamePlayers(game)
		topPlayer = Player()
		for player in self.playerList:
			if player.score>topPlayer.score:
				topPlayer=player
		message = []
		message.append("    ~ffffe630"+topPlayer.name + " is the player of the day! ")
		if (utilityObj.hasFinishedBoot):
			printerObj.printToBoard(message,"player")
		self.webPrefix="http://noahn.me"
		webPathSetPlayer = "/setPlayerOfDay?"
		message = topPlayer.name + " is the player of the day!"
		messengerObj.sendMessage(message,"playerOfDay")
		day,message,url=self.loadTopPlayerData(topPlayer.url)

		rval2 = requests.get(self.webPrefix + webPathSetPlayer + "day=" + day + "&message=" + message + "&url=" +  url) 

	
		return
	def startDay(self):
		self.gameList = []
		self.gamesOver=False
		self.gameOverCount=0
		#Retrieve the HTML for ESPN scoreboard
		printerObj.debugPrint("get request to " + 'http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		page = requests.get('http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		tree = html.fromstring(page.content);

		#Retrieve ids for each game on the current day.
		#An id is defined by ESPN as a unique numerical identifier for a given game
		#id is used to more directly access elements of the XML using XPATH
		idList = tree.xpath('//*[@id="content"]/*[@class="span-4"]/*/*/@id')
		#remove two video related html elements
		idList = idList[2:]
		#remove text off the id to leave just numerical id
		idList = [ x[:-8] for x in idList ]


		#Add each game to the games list with initialized data
		for id in idList:
			#find the urls of each game in the scoreboard. dissselect the recap headlines which are found similarly
			url = "http://espn.go.com" + str(tree.xpath('//*[@id="' + id +  '-gameLinks"]/a[1]/@href')[0])
			#retrieve remaining game data( not currently using homeScore or awayScore as it should start at 0-0). 
			homeScore = tree.xpath('//*[@id="' +  id +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  id +  '-awayHeaderScore"]/text()')[0]
			homeTeam = tree.xpath('//*[@id="' +  id +  '-homeHeader"]/td[1]/div/a/text()')[0]
			awayTeam = tree.xpath('//*[@id="' +  id +  '-awayHeader"]/td[1]/div/a/text()')[0]

			newGame = Game(awayTeam,homeTeam,url,id)
			self.gameList.append(newGame)

	#loops through games on a given day. Prints out info depending on if game is past,current or upcomming
	def printableGameList(self):
		leagueStr = []
		leagueStr.append("")
		strLen=0
		index=0;
		for game in self.gameList:
			gameStr=""
			if strLen > 132:
				strLen=0
				index=index+1
				leagueStr.append("")
			if not game.gameStarted:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " vs " + leagueObj.getFormattedTeamString(game.awayTeam) + " " + game.gameTime
				strLen+=16
			elif not game.gameEnded:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " " + leagueObj.getFormattedTeamString(game.awayTeam)
				strLen+=11
			else:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-"  +  str(game.awayScore) + " " +leagueObj.getFormattedTeamString(game.awayTeam)  +" " + game.gameStatusStr
				strLen+=17
			gameStr+="   ";
			strLen+=3
			leagueStr[index]+=gameStr
		return leagueStr
					
	#load the current score of all games of the day and compare to previous values
	def loadScoreboard(self):
		#Retreive HTML for ESPN Scoreboard
		time.sleep(1)
		printerObj.debugPrint("get request to " + 'http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		page = requests.get('http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		tree = html.fromstring(page.content);

		#For each game check score vs previous as well as game status
		gameHasChanged=False
		for game in self.gameList:
			homeScore = tree.xpath('//*[@id="' +  game.gameId +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  game.gameId +  '-awayHeaderScore"]/text()')[0]
			game.gameStatusStr=tree.xpath('//*[@id="'+ game.gameId + '-statusLine1"]/text()')[0]
			#homeScore = homeScore.encode("utf-8")
			if (not homeScore[0].isdigit()):#\xa0
				printerObj.debugPrint("game has not started")
				game.gameTime = tree.xpath('//*[@id="' +  game.gameId +  '-statusLine2Left"]/text()')
				if not game.gameTime:
					game.gameTime="POS"
					continue
				game.gameTime=game.gameTime[0].partition(' ')[0]
				hour=game.gameTime.partition(':')[0]
				minute=game.gameTime.partition(':')[2]
				hour=str(int(hour)-1)
				game.gameTime=hour+":"+minute

				continue
			elif (not game.gameStarted):
				printerObj.debugPrint("Game Just Started")
				game.gameStarted=True
			elif (not game.gameEnded and (game.gameStatusStr=='Final' or game.gameStatusStr=='Final/OT' or game.gameStatusStr=='Final/SO')):
				printerObj.debugPrint("Game Just Ended")
				self.gameOverCount=self.gameOverCount+1
				if self.gameOverCount==len(self.gameList):
					self.gamesOver=True
					utilityObj.readyForPlayerOfDay=True
				if (len(game.gameStatusStr)>5):
					game.gameStatusStr="F"+ game.gameStatusStr[5:]
				game.gameEnded = True
				self.loadGame(game,"")
				continue
			elif(game.gameEnded and game.numTimesChecked < 10):
				game.numTimesChecked=game.numTimesChecked+1
			elif(game.gameEnded and game.numTimesChecked >= 10):
				continue;
			#if score has changed, update score and send alert.
			scoringTeam = game.checkScore(int(awayScore),int(homeScore))
			if scoringTeam:
				printerObj.debugPrint("score change recognized!")
				gameHasChanged=True
				#retrieve information about scoring play
				self.loadGame(game,game.getScoringTeamName(scoringTeam))
		if not gameHasChanged:
			if not utilityObj.hasFinishedBoot:
				utilityObj.hasFinishedBoot=True;
			printerObj.printToBoard(self.printableGameList(),"Summary")
		
	#given game object for a game
	#find teams playing, scores, and most recent scoring play
	def loadGame(self, game,scoringTeamName):
		#Retreive the boxscore HTML from ESPN for a game
		time.sleep(1);
		printerObj.debugPrint("get request to " + game.url)
		page = requests.get(game.url)
		tree = html.fromstring(page.content);
		if  utilityObj.hasFinishedBoot:
			time.sleep(1);
		outputString = leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " "+ leagueObj.getFormattedTeamString(game.awayTeam) 

		if (not game.gameEnded):
			if (utilityObj.hasFinishedBoot):
				buzzerObj.startBuzzer(scoringTeamName)
			outputString+= " " + leagueObj.getFormattedTeamString(scoringTeamName) + " Goal! "
			#Retreive list of scorers in order (not(@colspan) removes penalty plays) //which div
			playList =  tree.xpath('//*[@id="my-players-table"]/*[@class="mod-container mod-no-header-footer mod-open mod-open-gamepack mod-box"]/div/table/*/*/td[3][not(@colspan)]/text()');
			finalPlaylist = []
			if (playList):
				tmpstr=""
				for tmpstr in playList:
					if tmpstr[0].isdigit():
						continue
					finalPlaylist.append(tmpstr)

			#Retreive list of assisters in order (0,1 or 2 can be given on a single line. 0 being unnasisted)
			playList2 =  tree.xpath('//*[@id="my-players-table"]/*[@class="mod-container mod-no-header-footer mod-open mod-open-gamepack mod-box"]/div/table/*/*/td[3]/i/text()');

			if finalPlaylist and playList2 and (len(finalPlaylist) == (game.homeScore+game.awayScore)):				
				#Concatonate last goal scorer and last assister and print this as the most recent scoring play
				mostRecent = " " + finalPlaylist[-1] + playList2[-1]
				outputString+=mostRecent
			outputString="     "+outputString
		else:
			if utilityObj.hasFinishedBoot:
				buzzerObj.startBuzzer("Default")
			outputString+=" " + game.gameStatusStr	
		outputList=[]
		outputList.append(outputString)
		if (utilityObj.hasFinishedBoot):
			printerObj.printToBoard(outputList,"action")

#retrive the headlines from NHL.com
def getNHLHeadlines():
	page = requests.get("https://www.nhl.com/")
	tree = html.fromstring(page.content);
	headlines = tree.xpath('//*[@id="content-wrap"]/div/div[3]/div[2]/section[1]/ul/*/a/text()')
	outputList=[]
	outputList.append(leagueObj.teamDict['Default']['hex'] + "30" + headlines)
	printerObj.printToBoard(outputList,"news")


class programUtilities:
	hasFinishedBoot=False
	readyForPlayerOfDay=False
	def __init__(self):		
		return


buzzerObj = Buzzer()
leagueObj = League()
printerObj = Printer()
messengerObj = Messenger()
utilityObj = programUtilities()
loadedDay=False


def getDateStr():
	dateStr = time.strftime("%Y%m%d") #oes this work for single digit days?
	curTime = time.strftime("%H")
	if int(curTime)<7:
		yesterday = datetime.date.today() - datetime.timedelta(1)
		dateStr=yesterday.strftime('%Y%m%d')
	#dateStr="20161015"
	return dateStr

#Main driver for program, runs until shut down.
def main():

	#str = "~ffffe630Hockey Ticker"
	#printerObj.printTest(str)#uncomment

	#initialize list of games
	scoreboard = ESPNSportsObj()
	loadedDay=True
	delay=10

	while True:
		#check each of the games for updated scores
		scoreboard.loadScoreboard()
		##wait x seconds for next check
		time.sleep(delay)
		printerObj.debugPrint("looping")
		if time.strftime("%H")==3:
			delay=60*60
		elif time.strftime("%H")==9:
			scoreboard.startDay()
		elif time.strftime("%H")==11:
			delay=10
		if (utilityObj.readyForPlayerOfDay):
			utilityObj.readyForPlayerOfDay=False
			scoreboard.loadDayPlayers()

	printerObj.debugPrint("ending")


#Test function that sends request directly to board
def testBoardCommunication():
	rval = requests.get(prefix+"G9hello world!")
	print(rval)

if __name__ == '__main__':
	main();
