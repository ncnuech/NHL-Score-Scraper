
#Class Describing data for an individual game
#Used to retrieve game data and check for score changes
class Game:
	#sortableGameStatus
	gameStatusInt=0

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
		#printerObj.debugPrint("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url

	def __init__(self,_awayTeam,_homeTeam,_url,_gameId,_proposedTime):
		#printerObj.debugPrint("running init on game")
		self.awayTeam = _awayTeam
		self.homeTeam = _homeTeam
		self.url = _url
		self.gameId = _gameId
		self.setGameTime(_proposedTime)

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

	def setGameTime(self,proposedTime):
		try:
			self.gameTime = proposedTime
			if not self.gameTime:
				if not self.gameEnded:
					self.gameTime="POS"
					self.gameStatusInt=0;
					return
				else:
					self.gameTime = "Game Over"
					self.gameStatusInt=13;
					return;
			self.gameTime=self.gameTime[0].partition(' ')[0]
			if not (self.gameTime):
				self.gameStatusInt=13;
				return
			if self.gameTime[1] != ":" and self.gameTime[2] != ":":
				if self.gameTime[-1]==",":
					self.gameTime=self.gameTime[:-1]
				self.gameStatusInt = 0;
				return;
			hour=self.gameTime.partition(':')[0]
			minute=self.gameTime.partition(':')[2]
			self.gameStatusInt = int(hour)+int(minute)/60;
			hour=str(int(hour)-1)
			if int(hour)<=0:
				hour=str(12+int(hour))
			self.gameTime=hour+":"+minute
		except:
			self.gameStatusInt = 13;
			self.gameTime = ""
			print("error in set Game Time")
		return