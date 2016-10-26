from Printer import Printer
import requests
import smtplib
class Messenger:
	webPrefixAction="http://noahn.me/getPhoneForActions?type="
	webPrefixPlayerOfDay="http://noahn.me/getPhoneForPlayerOfDay"

	def __init__(self):
		return

	def buildListAndSendMessage(self,message,type):
		phoneListStr=""
		try:
			phoneList = self.getPhoneList(type)
			if phoneList is None:
				return
		except requests.exceptions.RequestException as e:
			return
		self.sendMessage(message,phoneList)

	def sendMessage(self,message,phoneList):
		messageToSend = message
		server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login('noahnuechterlein@gmail.com','Felipe12')
		if not phoneList:
			return;
		for phone in phoneList:
			server.sendmail('noahnuechterlein@gmail.com',phone+'@vtext.com',messageToSend)
		server.quit()

	def getPhoneList(self,type):
		phoneListStr = requests.get(self.webPrefixAction + type)
		if phoneListStr.text=='':
			return []
		phoneList = phoneListStr.text.split(' ')
		return phoneList

	def parseTextFromBoardMessage(self,message):
			message=message[4:]
			messageList=message.split('~')
			finalMessage=""
			for msg in messageList:
				msg=msg[8:]
				finalMessage+=msg
			if len(finalMessage) <= 22:
				return finalMessage
			else:
				return finalMessage[:21]