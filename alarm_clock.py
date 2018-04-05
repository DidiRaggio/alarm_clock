#!usr/bin/env python  
#coding=utf-8  

import datetime, re
import pyaudio
import wave
import sys
import os.path
import time


class AlarmClock(object):
	"""AlarmClock takes an inputted string to set the the alarm time.
	and plays the corresponding sequence of wav files (of pre recorded words)
	 at the specified alarm time"""
	def __init__(self):
		super(AlarmClock, self).__init__()
		self.alarm_time_str = self.get_alarm_time()
		self.alarm_time_list = self.parse_alarm_time_str()
		self.wav_list = self.select_wav_files()
		self.sleep_time = self.determine_sleep_time()


	def get_alarm_time(self):
		""" get_alarm_time propts the user to enter a string,
		which is then verified to be in the correct format with regexp.
		"""
		time_pattern = re.compile(r'([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]')

		alarm_set = raw_input("Set alarm time (hh:mm): ")

		while not time_pattern.match(alarm_set):
			print('Invalid input. Must be expressed in "hh:mm"')
			alarm_set = raw_input("Set alarm time (hh:mm): ")

		print("THE ALARM HAS BEEN SET! :)")
		return alarm_set

	def parse_alarm_time_str(self):
		''' parse_alarm_time_str creates a list of [Hour, First Minute Digit, Second Minute Digit] 
				'''
		alarm_time_list = [ int(x) for x in self.alarm_time_str.split(":") ]
		try:
			alarm_time_list = [alarm_time_list[0],int(str(alarm_time_list[1])[0]), int(str(alarm_time_list[1])[1])]
		except:
			alarm_minutes = int(str(alarm_time_list[1])[0])
			if alarm_minutes == 0:
				alarm_time_list = [alarm_time_list[0], alarm_minutes, 0]
			else:
				alarm_time_list = [alarm_time_list[0], 0, alarm_minutes]
		return alarm_time_list

	def select_wav_files(self):
		''' select_wav_files reads the alart_time_list and determines what wav files to select.
				if the inputted time is AM or PM, if it adds the "oh" etc. '''
		# Initiate wav_list
		wav_list = []
		alarm_time_hour = self.alarm_time_list[0]
		alarm_time_minute1 = self.alarm_time_list[1]
		alarm_time_minute2 = self.alarm_time_list[2]

		# Determine if AM or PM
		if alarm_time_hour < 12:
			wav_list.insert(0, "./irishclock/am.wav")
		else:
			wav_list.insert(0, "./irishclock/pm.wav")
			# Adjust PM hour
			alarm_time_hour = alarm_time_hour - 12

		# Add hour to wav_list
		if alarm_time_hour == 0:
			wav_list.insert(0, "./irishclock/12.wav")
		else:
			wav_list.insert(0, "./irishclock/{}.wav".format(alarm_time_hour))

		# Add minutes to wav_list
		# No minutes
		if alarm_time_minute1 == 0 and alarm_time_minute2 == 0:
			pass
		# Single digit minutes
		elif alarm_time_minute1 == 0 and alarm_time_minute2 != 0:
			wav_list.insert(1, "./irishclock/o.wav")
			wav_list.insert(2, "./irishclock/{}.wav".format(alarm_time_minute2))
		# Minutes between 10 and 19
		elif alarm_time_minute1 == 1:
			wav_list.insert(1, "./irishclock/{0}{1}.wav".format(alarm_time_minute1, alarm_time_minute2))
		# Minutes over 19
		else:
			wav_list.insert(1, "./irishclock/{}0.wav".format(alarm_time_minute1))
			wav_list.insert(2, "./irishclock/{}.wav".format(alarm_time_minute2))

		wav_list.insert(0, "./irishclock/its.wav")

		return wav_list

	def determine_sleep_time(self):
		'''determine_sleep_time obtains the amount of seconds from the current time to the inputted alarm time'''
		FMT = '%H:%M'

		alarm_time = datetime.datetime.strptime(self.alarm_time_str, FMT)
		time_now = datetime.datetime.now()

		sleep_time = (alarm_time - time_now.replace(year=1900, month=01, day=01)).total_seconds()

		if sleep_time < 0:
			sleep_time += 86400
		
		return sleep_time

	CHUNK_SIZE = 1024

	def play_wav(self, wav_filename, chunk_size=CHUNK_SIZE):
		'''
		Play (on the attached system sound device) the WAV file
		named wav_filename.
		'''
		try:
			
			print( 'Trying to play file ' + wav_filename)
			wf = wave.open(wav_filename, 'rb')
		except IOError as ioe:
			sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
			str(ioe) + '. Skipping.\n')
			return
		except EOFError as eofe:
			sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
			str(eofe) + '. Skipping.\n')
			return

		# Instantiate PyAudio.
		p = pyaudio.PyAudio()

		# Open stream.
		stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			rate=wf.getframerate(),
			output=True,
			frames_per_buffer = wf.getsampwidth())
			# output=True)

		data = wf.readframes(chunk_size)
		while len(data) > 0:
			stream.write(data)
			data = wf.readframes(chunk_size)

		# Stop stream.
		stream.stop_stream()
		stream.close()

		# Close PyAudio.
		p.terminate()

	def run(self):
		time.sleep(sleep_time)
		for wav_filename in self.wav_list:
			self.play_wav(wav_filename)

if __name__ == '__main__':
	AlarmClock().run()