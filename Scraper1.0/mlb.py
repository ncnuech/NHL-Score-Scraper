#!/usr/bin/python3
from lxml import html
import requests

import os
import signal
import time

import threading
import subprocess

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

	#id used to identify a given game(most notibly used by ESPN.com)
	gameId = 0;

	#Constructor for a game, called once as "Game()"
	#_awayTeam --- name of away team
	#_homeTeam --- name of home team
	#_url --- url for further game details
	def __init__(self,_awayTeam,_homeTeam,_url):
		print("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url

	def __init__(self,_awayTeam,_homeTeam,_url,_gameId):
		print("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url
		self.gameId = _gameId

	#checks current score of game(passed in) with previously documented values
	#returns true if score has changed, else returns false
	#newAwayScore --- newest away team score to compare
	#newHomeScore --- newest home team score to compare
	def checkScore(self,newAwayScore,newHomeScore):
		if(newAwayScore != self.awayScore):
			print("away score changed")
			self.awayScore = newAwayScore
			buzzerObj.startBuzzer(self.awayTeam)
			return True
		elif (newHomeScore != self.homeScore):
			self.homeScore = newHomeScore
			buzzerObj.startBuzzer(self.homeTeam)
			print("home score changed")
			return True
		else:
			print("no score change")
			return False


###############################################
#Code to play sound (unfinished)
#threading starts a 2nd thread in a callback function
#code is using vlc in specific location on device
#call subprocess with vlc then shut down after x seconds
class Buzzer:

	#Current dictionary to hold team name to location of mp3 file for buzzer
	buzzerDict = {}


	#hardcoded paths to mp3 files
	#may make dict to teams and just use that in future
	def setupBuzzerDict(self):
		prefix = "BuzzerSounds/"
		self.buzzerDict["Blackhawks"] = prefix + "chicago.mp3"
		self.buzzerDict["Avalanche"] = prefix + "colorado.mp3"
		self.buzzerDict["Stars"] = prefix + "dallas.mp3"
		self.buzzerDict["Wild"] = prefix + "minnesota.mp3"
		self.buzzerDict["Predators"] = prefix + "nashville.mp3"
		self.buzzerDict["Blues"] = prefix + "stlouis.mp3"
		self.buzzerDict["Jets"] = prefix + "winnepeg.mp3"
		self.buzzerDict["Bruins"] = prefix + "boston.mp3"
		self.buzzerDict["Sabres"] = prefix + "buffalo.mp3"
		self.buzzerDict["Red Wings"] = prefix + "detroit.mp3"
		self.buzzerDict["Panthers"] = prefix + "florida.mp3"
		self.buzzerDict["Canadiens"] = prefix + "montreal.mp3"
		self.buzzerDict["Senators"] = prefix + "ottawa.mp3"
		self.buzzerDict["Lightning"] = prefix + "tampabay.mp3"
		self.buzzerDict["Maple Leafs"] = prefix + "toronto.mp3"
		self.buzzerDict["Ducks"] = prefix + "anaheim.mp3"
		self.buzzerDict["Coyotes"] = prefix + "arizona.mp3"
		self.buzzerDict["Flames"] = prefix + "calgary.mp3"
		self.buzzerDict["Oilers"] = prefix + "edmonton.mp3"
		self.buzzerDict["Kings"] = prefix + "losangeles.mp3"
		self.buzzerDict["Sharks"] = prefix + "sanjose.mp3"
		self.buzzerDict["Canucks"] = prefix + "vancouver.mp3"
		self.buzzerDict["Hurricanes"] = prefix + "carolina.mp3"
		self.buzzerDict["Blue Jackets"] = prefix + "columbus.mp3"
		self.buzzerDict["Devils"] = prefix + "newjersey.mp3"
		self.buzzerDict["Islanders"] = prefix + "newyorkislanders.mp3"
		self.buzzerDict["Rangers"] = prefix + "newyorkrangers.mp3"
		self.buzzerDict["Flyers"] = prefix + "philadelphia.mp3"
		self.buzzerDict["Penguins"] = prefix + "pittsburgh.mp3"
		self.buzzerDict["Capitals"] = prefix + "washington.mp3"

	#starts the buzzer when a specific team scores. must call with team name
	#uses vlc player right now. will have to work if go to rPI
	#currently 10 seconds to end buzzer
	#buzzers will play on top of each other
	def startBuzzer(self,teamName):
		sound_player = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
		sound_file = self.buzzerDict[teamName]
		music_player_subprocess = subprocess.Popen([sound_player,sound_file])
		threading.Timer(10.0,self.endBuzzer,[music_player_subprocess]).start()

	#call to end buzzer
	def endBuzzer(self,music_player_subprocess):
		os.kill(music_player_subprocess.pid, signal.SIGINT)

	def __init__(self):		
		#threading.Timer(.1,self.startBuzzer).start()
		self.setupBuzzerDict()
###############################################
class ESPNSportsObj:

	#List of Game Objects that hold  data on games on the current day
	#Current day is currently Hardcoded
	#TODO grab game on current date
	gameList = []

	def __init__(self):
		#Retrieve the HTML for ESPN scoreboard
		page = requests.get('http://www.foxsports.com/college-football/scores?season=2015&seasonType=1&week=1&group=0')
		tree = html.fromstring(page.content);

		#Retrieve ids for each game on the current day.
		#An id is defined by ESPN as a unique numerical identifier for a given game
		#id is used to more directly access elements of the XML using XPATH
		urlList = tree.xpath('//*[@id="wisbb_scoresContainer"]/div[1]/section[1]/footer/a[2]/@href')

		#Add each game to the games list with initialized data
		for url in urlList:
			#find the urls of each game in the scoreboard. dissselect the recap headlines which are found similarly
			url = "http://espn.go.com" + str(tree.xpath('//*[@id="' + id +  '-gameLinks"]/a[1]/@href')[0])
			#retrieve remaining game data( not currently using homeScore or awayScore as it should start at 0-0). 
			homeScore = tree.xpath('//*[@id="' +  id +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  id +  '-awayHeaderScore"]/text()')[0]
			homeTeam = tree.xpath('//*[@id="' +  id +  '-homeHeader"]/td[1]/div/a/text()')[0]
			awayTeam = tree.xpath('//*[@id="' +  id +  '-awayHeader"]/td[1]/div/a/text()')[0]

			newGame = Game(awayTeam,homeTeam,url,id)
			self.gameList.append(newGame)

	#load the current score of all games of the day and compare to previous values
	def loadScoreboard(self):
		#Retreive HTML for ESPN Scoreboard
		page = requests.get('http://espn.go.com/nhl/scoreboard?date=20160503')
		tree = html.fromstring(page.content);

		#For each game check score vs previous
		for game in self.gameList:
			homeScore = tree.xpath('//*[@id="' +  game.gameId +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  game.gameId +  '-awayHeaderScore"]/text()')[0]

			#if score has changed, update score and send alert.
			if  game.checkScore(int(awayScore),int(homeScore)):
				print("score change recognized!")
				#retrieve information about scoring play
				self.loadGame(game)

	#given game object for a game
	#find teams playing, scores, and most recent scoring play
	def loadGame(self, game):
		#Retreive the boxscore HTML from ESPN for a game
		page = requests.get(game.url)
		tree = html.fromstring(page.content);

		print(game.homeTeam + " " + str(game.homeScore) + " - " + game.awayTeam + " " + str(game.awayScore))
		#Retreive list of scorers in order (not(@colspan) removes penalty plays)
		playList =  tree.xpath('//*[@id="my-players-table"]/div[4]/div/table/*/*/td[3][not(@colspan)]/text()');
		#Retreive list of assisters in order (0,1 or 2 can be given on a single line. 0 being unnasisted)
		playList2 =  tree.xpath('//*[@id="my-players-table"]/div[4]/div/table/*/*/td[3]/i/text()');
		#Concatonate last goal scorer and last assister and print this as the most recent scoring play
		mostRecent = playList[-1] + playList2[-1]
		print(mostRecent);


buzzerObj = Buzzer()


#Main driver for program, runs until shut down.
def main():
	#initialize list of games

	scoreboard = ESPNSportsObj()

	while True:
		#check each of the games for updated scores
		scoreboard.loadScoreboard()
		##wait x seconds for next check
		time.sleep(30)
		print("looping")
	print("ending")


