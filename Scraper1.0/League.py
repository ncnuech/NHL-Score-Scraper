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
		self.teamDict["Jets"] = {"abbr":"WPG","buzzerFile":prefix + "winnepeg.mp3","hex":"~002e62"}
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

		self.teamDict["Chicago Blackhawks"] = self.teamDict["Blackhawks"];
		self.teamDict["Colorado Avalanche"] = self.teamDict["Avalanche"];
		self.teamDict["Dallas Stars"] = self.teamDict["Stars"]
		self.teamDict["Minnesota Wild"] = self.teamDict["Wild"]
		self.teamDict["Nashville Predators"] = self.teamDict["Predators"] 
		self.teamDict["St. Louis Blues"]  = self.teamDict["Blues"] 
		self.teamDict["Winnipeg Jets"] = self.teamDict["Jets"] 
		self.teamDict["Boston Bruins"] = self.teamDict["Bruins"]
		self.teamDict["Buffalo Sabres"] = self.teamDict["Sabres"]
		self.teamDict["Detroit Red Wings"] = self.teamDict["Red Wings"]
		self.teamDict["Florida Panthers"] = self.teamDict["Panthers"]
		self.teamDict["Montreal Canadiens"] = self.teamDict["Canadiens"]
		self.teamDict["Ottawa Senators"] = self.teamDict["Senators"] 
		self.teamDict["Tampa Bay Lightning"]  = self.teamDict["Lightning"] 
		self.teamDict["Toronto Maple Leafs"] = self.teamDict["Maple Leafs"]
		self.teamDict["Anaheim Ducks"] = self.teamDict["Ducks"]
		self.teamDict["Arizona Coyotes"] = self.teamDict["Coyotes"]
		self.teamDict["Calgary Flames"]  = self.teamDict["Flames"] 
		self.teamDict["Edmonton Oilers"] = self.teamDict["Oilers"]
		self.teamDict["Los Angeles Kings"]  = self.teamDict["Kings"] 
		self.teamDict["San Jose Sharks"] = self.teamDict["Sharks"]
		self.teamDict["Vancouver Canucks"] = self.teamDict["Canucks"]
		self.teamDict["Carolina Hurricanes"]= self.teamDict["Hurricanes"]
		self.teamDict["Columbus Blue Jackets"] = self.teamDict["Blue Jackets"]
		self.teamDict["New Jersey Devils"] = self.teamDict["Devils"]
		self.teamDict["New York Islanders"] = self.teamDict["Islanders"]
		self.teamDict["New York Rangers"] = self.teamDict["Rangers"]
		self.teamDict["Philadelphia Flyers"] = self.teamDict["Flyers"]
		self.teamDict["Pittsburgh Penguins"] = self.teamDict["Penguins"]
		self.teamDict["Washington Capitals"] = self.teamDict["Capitals"]

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
