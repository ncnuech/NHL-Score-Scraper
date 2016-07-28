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
	#Boolean for whether game has started True if started
	gameStarted = False;
	#Boolean for whether game has ended True if ended
	gameEnded = False;

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
			return True
		elif (newHomeScore != self.homeScore):
			self.homeScore = newHomeScore
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
	def __init__(self,):		
		threading.Timer(.1,self.startBuzzer).start()

	def startBuzzer():
		sound_player = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
		sound_file = "BuzzerSounds/arizona.mp3"
		music_player_subprocess = subprocess.Popen([sound_player,sound_file])
		threading.Timer(10.0,self.endBuzzer,[music_player_subprocess]).start()

	def endBuzzer(music_player_subprocess):
		os.kill(music_player_subprocess.pid, signal.SIGINT)
###############################################

class ESPNSportsObj:

	gameList = []

	def __init__(self):
		page = requests.get('http://espn.go.com/nhl/scoreboard?date=20160503')
		tree = html.fromstring(page.content);
		#find the urls of each game in the scoreboard. dissselect the recap headlines which are found similarly
		idList = tree.xpath('//*[@id="content"]/*[@class="span-4"]/*/*/@id')
		idList = idList[2:]
		idList = [ x[:-8] for x in idList ]

		for id in idList:
			url = "http://espn.go.com" + str(tree.xpath('//*[@id="' + id +  '-gameLinks"]/a[1]/@href')[0])
			homeScore = tree.xpath('//*[@id="' +  id +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  id +  '-awayHeaderScore"]/text()')[0]
			homeTeam = tree.xpath('//*[@id="' +  id +  '-homeHeader"]/td[1]/div/a/text()')[0]
			awayTeam = tree.xpath('//*[@id="' +  id +  '-awayHeader"]/td[1]/div/a/text()')[0]

			newGame = Game(awayTeam,homeTeam,url,id)
			self.gameList.append(newGame)

	def loadScoreboard(self):
		page = requests.get('http://espn.go.com/nhl/scoreboard?date=20160503')
		tree = html.fromstring(page.content);
		for game in self.gameList:
			homeScore = tree.xpath('//*[@id="' +  game.gameId +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  game.gameId +  '-awayHeaderScore"]/text()')[0]

			if  game.checkScore(int(awayScore),int(homeScore)):
				print("score change recognized!")
				#retrieve information about scoring play
				self.loadGame(game)
	def loadGame(self, game):
		page = requests.get(game.url)
		tree = html.fromstring(page.content);

		print(game.homeTeam + " " + str(game.homeScore) + " - " + game.awayTeam + " " + str(game.awayScore))
		playList =  tree.xpath('//*[@id="my-players-table"]/div[4]/div/table/*/*/td[3][not(@colspan)]/text()');
		playList2 =  tree.xpath('//*[@id="my-players-table"]/div[4]/div/table/*/*/td[3]/i/text()');
		mostRecent = playList[-1] + playList2[-1]
		print(mostRecent);


#Out of date!. Yahoo changed scoreboard site. Boxscores should still work
class YahooSportsObj:

	scoreboardGamePanelURL = '//*[@id="mediasportsscoreboardgrandslam"]/*/*/*/*'

	gameList = []

	#load the initial game data 
	#using xpath, scrape and retrieve html text data from yahoo sports
	#TODO grabs data from a specific date 
	def __init__(self):
		page = requests.get('http://sports.yahoo.com/nhl/scoreboard/')
		tree = html.fromstring(page.content);
		#to describe the first xpath function we are retriving anything xml tag with the id "mediasports..." 
		#then through the hierarchy, anything->anything->anything->anything and then return the value of the attribute data-url at that point
		urlList = tree.xpath('//*[@id="scoreboard-group-2"]/div/ul/*/div/div/a/@href')
		scores = tree.xpath('//*[@id="mediasportsscoreboardgrandslam"]/*/*/*/*/td[@class="score"]/*/*/*/text()')
		aways = tree.xpath('//*[@id="mediasportsscoreboardgrandslam"]/*/*/*/*/td[@class="away"]/*/em/text()')
		homes = tree.xpath('//*[@id="mediasportsscoreboardgrandslam"]/*/*/*/*/td[@class="home"]/*/em/text()')
		#iterate through each game initializing game objects and adding them to global gameList
		for i in range(len(aways)): 
			print("here")
			fullUrl = "http://sports.yahoo.com" + urlList[i];
			newGame = Game(aways[i],homes[i],fullUrl)
			self.gameList.append(newGame)

		print(len(self.gameList))

	#load the current score of all games of the day and compare to previous values
	#Out of Date
	def loadScoreboard(self):
		page = requests.get('http://sports.yahoo.com/nhl/scoreboard/')
		tree = html.fromstring(page.content);
		#scores --- scores of all games of the day in away,home,away,home order
		scores = tree.xpath('//*[@id="mediasportsscoreboardgrandslam"]/*/*/*/*/td[@class="score"]/*/*/*/text()')
		#index moves by two through scores(one game at a time)
		index = 0
		print("gogogo")
		#loop through all games from the day
		for game in self.gameList:
			#check if game score has changed from saved values
			print("here")
			if  game.checkScore(int(scores[index]),int(scores[index+1])):
				print("score change recognized!")
				#retrieve information about scoring play
				self.loadGame(game.url)
			index += 2

	#given a url for a game
	#find teams playing, scores, and most recent scoring play
	def loadGame(self, boxscoreLink):
		page = requests.get(boxscoreLink)
		tree = html.fromstring(page.content);

		teams = tree.xpath('//*[@id="Col1-0-Boxscore"]/div[1]/div[3]/div/div/div[1]/div/div[2]/div[1]/a/span/text()')
		teams += tree.xpath('//*[@id="Col1-0-Boxscore"]/div[1]/div[3]/div/div/div[2]/div/div[2]/div[1]/a/span/text()')
		print('Teams: ' + str(teams))

		scores = tree.xpath('//*[@id="Col1-0-Boxscore"]/div[1]/div[3]/div/div/div[1]/div/span/text()')
		scores += tree.xpath('//*[@id="Col1-0-Boxscore"]/div[1]/div[3]/div/div/div[2]/div/span/text()')
		print('Scores: ' + str(scores))

		playList =  tree.xpath('//*[@id="Col1-0-Boxscore"]/div[4]/div[2]/*/table/tbody/*/td[3]/text()');
		mostRecent = playList[-1]
		print(mostRecent);


#retrive the headlines from NHL.com
def getNHLHeadlines():
	page = requests.get("https://www.nhl.com/")
	tree = html.fromstring(page.content);
	headlines = tree.xpath('//*[@id="content-wrap"]/div/div[3]/div[2]/section[1]/ul/*/a/text()')
	print(headlines)

#Main driver for program, runs until shut down.
def main():
	#initialize list of games
	#yahooSetupScoreboard()
	#scoreboard = YahooSportsObj()
	scoreboard = ESPNSportsObj()
	while True:
		#check each of the games for updated scores
		#yahooScoreboard()
		scoreboard.loadScoreboard()
		##wait x seconds for next check
		time.sleep(30)
		print("looping")
	print("ending")

if __name__ == '__main__':
	print("starting")
	main();