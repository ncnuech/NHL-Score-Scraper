import threading
import subprocess
import time
import os
import signal

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
	def startBuzzer(self,teamName,sound_file):
		time.sleep(10)

		playTime=10
		if (teamName=="Default"):
			playTime=8
		if os.name=="nt":
			sound_player = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
		else:
			sound_player = "/usr/bin/cvlc"
		print("file" + sound_file)
		music_player_subprocess = subprocess.Popen([sound_player,sound_file])
		threading.Timer(10.0,self.endBuzzer,[music_player_subprocess]).start()

	#call to end buzzer
	def endBuzzer(self,music_player_subprocess):
		os.kill(music_player_subprocess.pid, signal.SIGINT)

	def __init__(self):		
		return
