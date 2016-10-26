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



import calendar


from Utility import programUtilities
from game import Game
from League import League
from Buzzer import Buzzer
from Messenger import Messenger
from Player import Player
from Printer import Printer

class ESPNSportsObj:

	#List of Game Objects that hold  data on games on the current day
	#Current day is currently Hardcoded
	#TODO grab game on current date
	gameList = []
	gamesOver = False
	gameOverCount=0
	playerList = []
	anyGameHasStarted = False
	def __init__(self):
		self.startDay()

	
	def loadGamePlayers(self,game):
		printerObj.debugPrint("get request to " + game.url)
		try:
			page = requests.get(game.url)
		except requests.exceptions.RequestException as e:
			print("Error in load game players")
			return
		tree = html.fromstring(page.content);

		playerStats =  tree.xpath('//*[@id="my-players-table"]/*/div[2]/table/thead/tr/td/*/div/table/tbody[1]/*');
		for player in playerStats:
			try:
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
			except:
				continue
		playerStats =  tree.xpath('//*[@id="my-players-table"]/*/div[2]/table/thead/tr/*/div/div/table/tbody/*')
		first=True
		for player in playerStats:
			try:
				if not player.xpath('td[1]/a/text()') or not player.xpath('td[6]/text()'):
					tempPlayer = player.xpath('td[1]/a/text()')
					continue;
				name = player.xpath('td[1]/a/text()')[0]
				url = player.xpath('td[1]/a/@href')[0]
				goalsAllowed=int(player.xpath('td[3]/text()')[0])
				saveper=float(player.xpath('td[5]/text()')[0])
				toi=player.xpath('td[6]/text()')[0]
				minutes=int(toi.split(':')[0])
				if minutes<30:
					continue
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
			except:
				continue
		return

	def pluralizeStats(self,stat,tag):
		if stat==1:
			stats = str(stat) + " " + tag + ", "
		else:
			stats = str(stat) + " " +tag + "s, "
		return stats

	def loadTopPlayerData(self,url,player):
		printerObj.debugPrint("get request to " + url + "   " +  str(player.score))
		try:
			page = requests.get(url)
		except requests.exceptions.RequestException as e:
			print("error in loadTopPlayerData")
			return
		tree = html.fromstring(page.content);
		try:
			if ( tree.xpath('//*[@id="content"]/div[3]/div[2]/div[2]/img/@src')):
				imgurl =  tree.xpath('//*[@id="content"]/div[3]/div[2]/div[2]/img/@src')[0];
				name = tree.xpath('//*[@id="content"]/div[3]/div[2]/h1/text()')[0];
				team = tree.xpath('//*[@id="content"]/div[3]/div[2]/div[3]/ul[1]/li[3]/a/text()')[0]
			else:
				imgurl=""
				name = tree.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/h1/text()')[0];
				team = tree.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/ul[1]/li[3]/a/text()')[0]
				print("no image")
		except:
			imgurl=""
			name=""
			team="Detroit Red Wings"
			print("error in loading players")
		#color = tree.xpath('//*[@id="content"]/div[3]/div[2]/div[4]/table/thead/tr/th[3]');
		date = "Friday October 14th"
		teamAbbr = leagueObj.teamDict[team]['abbr'].lower()
		teamPic = "http://a.espncdn.com/combiner/i?img=/i/teamlogos/nhl/500-dark/" + teamAbbr + ".png"
		stats = "("
		if player.skater:
			stats = stats+ self.pluralizeStats(player.goals,"Goal")
			stats = stats + self.pluralizeStats(player.assists,"Assist")
			if player.plusminus > 0:
				stats = stats + "^" + str(player.plusminus) + ", "
			elif player.plusminus==0:
				stats = stats +  "(^/-)" + str(player.plusminus) + ", "
			else:
				stats = stats + str(player.plusminus) + ", "
			stats = stats + str(player.pim) + " PIM, "
			stats = stats + str(player.sog) + " SOG"
		else:
			stats = stats + str(round(player.gaa,2)) + " GAA "
			if player.wins==1:
				stats = stats + "Win, "
			stats = stats + str(round(player.saveper,3)) + " SV%"
			if player.so==1:
				stats = stats + " SO"
		stats = stats + ")"
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
		return date,name,imgurl,stats,teamPic

	def findTopPlayer(self,num):
		self.playerList=[]
		for game in self.gameList:
			try:
				self.loadGamePlayers(game)
			except:
				print("error in find top player")
				continue;
		topPlayer = Player()
		self.playerList = sorted(self.playerList, key=lambda Player: Player.score,reverse=True)
		topPlayers = []
		for i in range(num):
			if (i >= len(self.playerList)):
				topPlayers.append("")
			else:
				topPlayers.append(self.playerList[i])
		return topPlayers

	def loadUnfinishedDayPlayers(self):

		topPlayers = self.findTopPlayer(3)
		day = ""
		nameStr = ""
		urlStr=""
		statsStr=""
		teamPicStr=""
		for i in range(len(topPlayers)):
			try:
				day,name,url,stats,teamPic=self.loadTopPlayerData(topPlayers[i].url,topPlayers[i])
			except:
				print("name")
			statsStr= statsStr+ stats+ "_"
			nameStr=nameStr+name+"_"
			urlStr=urlStr+url.split('&')[0]+"_"
			teamPicStr = teamPicStr + teamPic+"_"
		nameStr=nameStr[:-1]
		urlStr=urlStr[:-1]
		statsStr = statsStr[:-1]
		teamPicStr = teamPicStr[:-1]
		worstDay,worstName,worstUrl,worstStats,worstTeamPic=self.loadTopPlayerData(self.playerList[-1].url,self.playerList[-1])
		self.webPrefix="http://noahn.me"
		webPathSetPlayer = "/setCurPlayerOfDay?"
		try:
			rval2 = requests.get(self.webPrefix + webPathSetPlayer + "day=" + day + "&message=" + nameStr + "&url=" +  urlStr + "&stats=" + statsStr + "&teamPic="+teamPicStr) 
		except requests.exceptions.RequestException as e:
			print("error in curplayerofday");
		return

	def loadDayPlayers(self):
		topPlayer = self.findTopPlayer(1)[0]
		day,webmessage,url,stats,teamPic=self.loadTopPlayerData(topPlayer.url,topPlayer)
		message = []
		message.append("    ~ffffe630"+topPlayer.name + " is the player of the day! " + stats.replace('^','+'))
		if (utilityObj.hasFinishedBoot):
			printerObj.printToBoard(message,"player")
		self.webPrefix="http://noahn.me"
		webPathSetPlayer = "/setPlayerOfDay?"
		message = topPlayer.name + " is the player of the day! "
		messengerObj.buildListAndSendMessage(message[0],"playerOfDay")
		try:
			rval2 = requests.get(self.webPrefix + webPathSetPlayer + "day=" + day + "&message=" + webmessage + "&url=" +  url + "&stats=" + stats) 
		except requests.exceptions.RequestException as e:
			print("error in loadDayPlayers")
	
		return


	def startDay(self):
		self.gameList = []
		self.gamesOver=False
		self.gameOverCount=0
		
		#Retrieve the HTML for ESPN scoreboard
		printerObj.debugPrint("get request to " + 'http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		try:
			page = requests.get('http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		except:
			return;
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
			url = "http://espn.go.com/nhl/boxscore?gameId=" + str(id)
			#retrieve remaining game data( not currently using homeScore or awayScore as it should start at 0-0). 
			homeScore = tree.xpath('//*[@id="' +  id +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  id +  '-awayHeaderScore"]/text()')[0]
			homeTeam = tree.xpath('//*[@id="' +  id +  '-homeHeader"]/td[1]/div/a/text()')[0]
			awayTeam = tree.xpath('//*[@id="' +  id +  '-awayHeader"]/td[1]/div/a/text()')[0]
			proposedTime = tree.xpath('//*[@id="' +  id +  '-statusLine2Left"]/text()')
			newGame = Game(awayTeam,homeTeam,url,id,proposedTime)
			self.gameList.append(newGame)
		self.gameList = sorted(self.gameList, key=lambda Game: Game.gameStatusInt,reverse=False)

		return

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
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " " + leagueObj.getFormattedTeamString(game.awayTeam) + " " + game.gameTime
				strLen+=17
			else:
				gameStr+=leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-"  +  str(game.awayScore) + " " +leagueObj.getFormattedTeamString(game.awayTeam)  +" " + game.gameStatusStr
				strLen+=18
			gameStr+="   ";
			strLen+=3
			leagueStr[index]+=gameStr
		return leagueStr

	#load the current score of all games of the day and compare to previous values
	def loadScoreboard(self):
		#Retreive HTML for ESPN Scoreboard
		printerObj.debugPrint("get request to " + 'http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		try:
			page = requests.get('http://espn.go.com/nhl/scoreboard?date='+getDateStr())
		except requests.exceptions.RequestException as e:
			print("error in loadScoreboard")
			return;
		tree = html.fromstring(page.content);

		#For each game check score vs previous as well as game status
		gameHasChanged=False
		for game in self.gameList:
			homeScore = tree.xpath('//*[@id="' +  game.gameId +  '-homeHeaderScore"]/text()')[0]
			awayScore = tree.xpath('//*[@id="' +  game.gameId +  '-awayHeaderScore"]/text()')[0]
			game.gameStatusStr=tree.xpath('//*[@id="'+ game.gameId + '-statusLine1"]/text()')[0]
			proposedTime = tree.xpath('//*[@id="' +  game.gameId +  '-statusLine2Left"]/text()')
			game.setGameTime(proposedTime)
			#homeScore = homeScore.encode("utf-8")
			if (not homeScore[0].isdigit()):#\xa0
				printerObj.debugPrint("game has not started")
				continue
			elif (not game.gameStarted):
				printerObj.debugPrint("Game Just Started")
				self.anyGameHasStarted=True;
				game.gameStarted=True
			elif (not game.gameEnded and (game.gameStatusStr=='Final' or game.gameStatusStr=='Final/OT' or game.gameStatusStr=='Final/SO')):
				if (int(homeScore)==int(awayScore)):
					# this may need debugging
					continue;
				printerObj.debugPrint("Game Just Ended")
				self.gameOverCount=self.gameOverCount+1
				if self.gameOverCount==len(self.gameList):
					self.gamesOver=True
					utilityObj.readyForPlayerOfDay=True
					self.anyGameHasStarted=False;
				if (len(game.gameStatusStr)>5):
					game.gameStatusStr="F"+ game.gameStatusStr[5:]
				game.gameEnded = True
				self.loadGame(game,"Default")
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
		if self.anyGameHasStarted:
			self.loadUnfinishedDayPlayers()

	#given game object for a game
	#find teams playing, scores, and most recent scoring play
	def loadGame(self, game,scoringTeamName):
		#Retreive the boxscore HTML from ESPN for a game
		printerObj.debugPrint("get request to " + game.url)
		try:
			page = requests.get(game.url)
		except requests.exceptions.RequestException as e:
			print("error in load game")
			time.sleep(5)
			self.loadGame(game,scoringTeamName)
			return
		tree = html.fromstring(page.content);

		outputString = leagueObj.getFormattedTeamString(game.homeTeam) + " " + str(game.homeScore) + "-" + str(game.awayScore) + " "+ leagueObj.getFormattedTeamString(game.awayTeam) 
		if (not game.gameEnded):
			outputString+= " " + leagueObj.getFormattedTeamString(scoringTeamName) + " Goal! "
			shortOutput = outputString + " "
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
				shortOutput+= " " + finalPlaylist[-1]
			outputString="     "+outputString
			shortOutput="     "+shortOutput
		else:
			outputString+=" " + game.gameStatusStr	
			shortOutput = "     " + outputString
		outputList=[]
		outputList.append(outputString)
		if (utilityObj.hasFinishedBoot):
			buzzerObj.startBuzzer(scoringTeamName,leagueObj.teamDict[scoringTeamName]['buzzerFile'])
			printerObj.printToBoard(outputList,"action")
			textMessage = messengerObj.parseTextFromBoardMessage(shortOutput)
			messengerObj.buildListAndSendMessage(textMessage,"action")


#retrive the headlines from NHL.com
def getNHLHeadlines():
	page = requests.get("https://www.nhl.com/")
	tree = html.fromstring(page.content);
	headlines = tree.xpath('//*[@id="content-wrap"]/div/div[3]/div[2]/section[1]/ul/*/a/text()')
	outputList=[]
	outputList.append(leagueObj.teamDict['Default']['hex'] + "30" + headlines)
	printerObj.printToBoard(outputList,"news")





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
	#initialize list of games
	scoreboard = ESPNSportsObj()
	loadedDay=True
	delay=0
	ignoreLoad=False
	while True:
		try:
				#check each of the games for updated scores

			if (not ignoreLoad):
				scoreboard.loadScoreboard()
			else:
				ignoreLoad = False;
			time.sleep(delay)

			##wait x seconds for next check
			printerObj.debugPrint("looping")
			if (int(time.strftime("%H"))==3):
				printerObj.clearBoard()
				ignoreLoad = True;
			if int(time.strftime("%H"))==7:
				scoreboard.startDay()

			if int(time.strftime("%H")) >= 3 and int(time.strftime("%H")) <11:
				delay=60*60
			elif int(time.strftime("%H")) > 11 or int(time.strftime("%H")) < 3:
				delay=10
			if (utilityObj.readyForPlayerOfDay):
				utilityObj.readyForPlayerOfDay=False
				scoreboard.loadUnfinishedDayPlayers()
				scoreboard.loadDayPlayers()

		except:
			print("error in main" )
			time.sleep(10);
			continue;


#Test function that sends request directly to board
def testBoardCommunication():
	rval = requests.get(prefix+"G9hello world!")
	print(rval)

if __name__ == '__main__':
	main();
