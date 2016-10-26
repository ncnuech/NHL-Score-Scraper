import requests
import time

class Printer:
	lastPrintWasSummary=False

	prefix="http://10.177.105.138/arduino/text/"
	webPrefix="http://noahn.me/getMessage?message="
	brightness="30"


	def __init__(self):
		return

	def printToBoard(self,outStr,type):
		print("\n")
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
			try:
				rval = requests.get(strComponent)#uncomment
				rval2 = requests.get(self.webPrefix+outStr[0])
			except:
				print("error in printToBoard")
				return;

			time.sleep(15)
		print("\n")


	def printTest(self,outStr):
		rval = requests.get(self.prefix+outStr)
		return

	def clearBoard(self):
		try:
				rval = requests.get(self.prefix + "~00000000")
		except:
			print("error clearing board")
			time.sleep(5);
			self.clearBoard();
		return;

	def debugPrint(self,outStr):
		print("\tdebug:\t"+outStr)




