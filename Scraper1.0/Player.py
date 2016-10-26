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
		self.score=self.wins*1.0+(2-self.gaa)+self.so*1.0+(self.saveper-.9)*10
		return
	def __init__(self):		
		return
