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

class Printer:

	#prefix="http://10.177.105.74:81/text/"
	prefix="http://10.177.105.137/arduino/text/"
	color="G"
	brightness="30"

	#Color Then 0-9
	def __init__(self):
		return

	def printToBoard(self,outStr):
		print("\n")
		print(self.prefix+outStr)
		rval = requests.get(self.prefix+outStr)
		time.sleep(15)
		print("\n")


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
		self.teamDict["Blackhawks"] = {"abbr":"CHI","buzzerFile":prefix+ "chicago.mp3","hex":"~e41836"}
		self.teamDict["Avalanche"] = {"abbr":"COL","buzzerFile":prefix + "colorado.mp3","hex":"~870038"}
		self.teamDict["Stars"] = {"abbr":"DAL","buzzerFile": prefix + "dallas.mp3","hex":"~03613f"}
		self.teamDict["Wild"] ={"abbr":"MIN","buzzerFile":prefix + "minnesota.mp3","hex":"~164734"}
		self.teamDict["Predators"] = {"abbr":"NSH","buzzerFile":prefix + "nashville.mp3","hex":"~ffb71a"}
		self.teamDict["Blues"] = {"abbr":"STL","buzzerFile":prefix + "stlouis.mp3","hex":"~083377"}
		self.teamDict["Jets"] = {"abbr":"WIN","buzzerFile":prefix + "winnepeg.mp3","hex":"~002e62"}
		self.teamDict["Bruins"] = {"abbr":"BOS","buzzerFile":prefix+"boston.mp3","hex":"~fcb930"}
		self.teamDict["Sabres"] = {"abbr":"BUF","buzzerFile":prefix+"buffalo.mp3","hex":"~f2b434"}
		self.teamDict["Red Wings"] = {"abbr":"DET","buzzerFile":prefix+ "detroit.mp3","hex":"~d42234"}
		self.teamDict["Panthers"] = {"abbr":"FLA","buzzerFile":prefix+"florida.mp3","hex":"~c49818"}
		self.teamDict["Canadiens"] = {"abbr":"MTL","buzzerFile":prefix+"montreal.mp3","hex":"~c51230"}
		self.teamDict["Senators"] = {"abbr":"OTT","buzzerFile":prefix+"ottawa.mp3","hex":"~d4a00f"}
		self.teamDict["Lightning"] = {"abbr":"TB","buzzerFile":prefix+"tampabay.mp3","hex":"~ffffff"}
		self.teamDict["Maple Leafs"] = {"abbr":"TOR","buzzerFile":prefix+"toronto.mp3","hex":"~013e7f"}
		self.teamDict["Ducks"] = {"abbr":"ANA","buzzerFile":prefix+"anaheim.mp3","hex":"~b6985a"}
		self.teamDict["Coyotes"] = {"abbr":"ARI","buzzerFile":prefix+ "arizona.mp3","hex":"~98012e"}
		self.teamDict["Flames"] = {"abbr":"CGY","buzzerFile":prefix+ "calgary.mp3","hex":"~cb0d0d"}
		self.teamDict["Oilers"] = {"abbr":"EDM","buzzerFile":prefix+ "edmonton.mp3","hex":"~eb6e1e"}
		self.teamDict["Kings"] = {"abbr":"LA","buzzerFile":prefix+"losangeles.mp3","hex":"~231f20"}
		self.teamDict["Sharks"] = {"abbr":"SJ","buzzerFile":prefix+"sanjose.mp3","hex":"~006e76"}
		self.teamDict["Canucks"] = {"abbr":"VAN","buzzerFile":prefix+"vancouver.mp3","hex":"~013e7f"}
		self.teamDict["Hurricanes"] = {"abbr":"CAR","buzzerFile":prefix+"carolina.mp3","hex":"~da2e2a"}
		self.teamDict["Blue Jackets"] = {"abbr":"CLS","buzzerFile":prefix+"columbus.mp3","hex":"~002e62"}
		self.teamDict["Devils"] = {"abbr":"NJ","buzzerFile":prefix+"newjersey.mp3","hex":"~ff0000"}
		self.teamDict["Islanders"] = {"abbr":"NYI","buzzerFile":prefix+"newyorkislanders.mp3","hex":"~f57d31"}
		self.teamDict["Rangers"] = {"abbr":"NYR","buzzerFile":prefix+"newyorkrangers.mp3","hex":"~005dab"}
		self.teamDict["Flyers"] = {"abbr":"PHI","buzzerFile":prefix+"philadelphia.mp3","hex":"~f37737"}
		self.teamDict["Penguins"] = {"abbr":"PIT","buzzerFile":prefix+"pittsburgh.mp3","hex":"~7ed5fa"}
		self.teamDict["Capitals"] = {"abbr":"WSH","buzzerFile":prefix+"washington.mp3","hex":"~e51837"}
		self.teamDict["Default"] = {"abbr":"DEF","buzzerFile":prefix+"hartford.mp3","hex":"~ffffe6"}


	def getFormattedTeamString(self,teamName):
		defaultBrightness="30"
		return self.teamDict[teamName]['hex'] + defaultBrightness + self.teamDict[teamName]['abbr'] + self.teamDict['Default']['hex'] + defaultBrightness

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
		if os.name=="nt":
			sound_player = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
		else:
			sound_player = "/usr/bin/cvlc"
		sound_file = leagueObj.teamDict[teamName]['buzzerFile']
		music_player_subprocess = subprocess.Popen([sound_player,sound_file])
		threading.Timer(10.0,self.endBuzzer,[music_player_subprocess]).start()

	#call to end buzzer
	def endBuzzer(self,music_player_subprocess):
		os.kill(music_player_subprocess.pid, signal.SIGINT)

	def __init__(self):		
		return
###############################################

class ESPNSportsObj:

	#List of Game Objects that hold  data on games on the current day
	#Current day is currently Hardcoded
	#TODO grab game on current date
	gameList = []

	def __init__(self):
		self.startDay()

	def startDay(self):
		self.gameList = []
		#Retrieve the HTML for ESPN scoreboard
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
		leagueStr = ""
		for game in self.gameList:
			gameStr=""
			if not game.gameStarted:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " vs " + leagueObj.getFormattedTeamString(game.awayTeam) + " " + game.gameTime
			elif not game.gameEnded:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " " + leagueObj.getFormattedTeamString(game.awayTeam)
			else:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-"  +  str(game.awayScore) + " " +leagueObj.getFormattedTeamString(game.awayTeam)  +" " + game.gameStatusStr
			gameStr+="   ";
			leagueStr+=gameStr
		return leagueStr
					
	#load the current score of all games of the day and compare to previous values
	def loadScoreboard(self):
		#Retreive HTML for ESPN Scoreboard
		page = requests.get('http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		tree = html.fromstring(page.content);

		#For each game check score vs previous as well as game status
		gameHasChanged=False
		for game in self.gameList:
			if (game.gameEnded):
			    continue
			homeScore = tree.xpath('//*[@id="' +  game.gameId +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  game.gameId +  '-awayHeaderScore"]/text()')[0]
			game.gameStatusStr=tree.xpath('//*[@id="'+ game.gameId + '-statusLine1"]/text()')[0]
			#homeScore = homeScore.encode("utf-8")
			if (not homeScore[0].isdigit()):#\xa0
				printerObj.debugPrint("game has not started")
				game.gameTime = tree.xpath('//*[@id="' +  game.gameId +  '-statusLine2Left"]/text()')[0]
				continue
			elif (not game.gameStarted):
				printerObj.debugPrint("Game Just Started")
				game.gameStarted=True
			elif (not game.gameEnded and (game.gameStatusStr=='Final' or game.gameStatusStr=='Final/OT')):
				printerObj.debugPrint("Game Just Ended")
				game.gameEnded = True
				self.loadGame(game,"")
				continue
			#if score has changed, update score and send alert.
			scoringTeam = game.checkScore(int(awayScore),int(homeScore))
			if scoringTeam:
				printerObj.debugPrint("score change recognized!")
				gameHasChanged=True
				#retrieve information about scoring play
				self.loadGame(game,game.getScoringTeamName(scoringTeam))
		if not gameHasChanged:
			printerObj.printToBoard(self.printableGameList())
	#given game object for a game
	#find teams playing, scores, and most recent scoring play
	def loadGame(self, game,scoringTeamName):
		#Retreive the boxscore HTML from ESPN for a game
		page = requests.get(game.url)
		tree = html.fromstring(page.content);
		outputString = leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " "+ leagueObj.getFormattedTeamString(game.awayTeam) 

		if (not game.gameEnded):
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
			outputString+=" " + game.gameStatusStr	
		printerObj.printToBoard(outputString)

#retrive the headlines from NHL.com
def getNHLHeadlines():
	page = requests.get("https://www.nhl.com/")
	tree = html.fromstring(page.content);
	headlines = tree.xpath('//*[@id="content-wrap"]/div/div[3]/div[2]/section[1]/ul/*/a/text()')
	printerObj.printToBoard(leagueObj.teamDict['Default']['hex'] + "30" + headlines)

buzzerObj = Buzzer()
leagueObj = League()
printerObj = Printer()
def getDateStr():
	dateStr = time.strftime("%Y%m%d") #oes this work for single digit days?
	#dateStr="20161002"
	curTime = time.strftime("%H")
	if int(curTime)<7:
		dateStr=str(int(dateStr)-1)
	return dateStr

#Main driver for program, runs until shut down.
def main():
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
	printerObj.debugPrint("ending")


#Test function that sends request directly to board
def testBoardCommunication():
	prefix="http://10.177.105.74:81/text/"
	prefix="http://10.177.105.137/arduino/ledText2/"
	rval = requests.get(prefix+"G9hello world!")
	print(rval)

if __name__ == '__main__':
	main();
