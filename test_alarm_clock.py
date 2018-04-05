import unittest
import sys
from alarm_clock import AlarmClock
import StringIO
import mock
import __builtin__
from freezegun import freeze_time



@freeze_time("2015-10-21 16:29:00")
class TestAlarmClock(unittest.TestCase):
	#CREATE METHODS TO INITIALIZE TESTING EXAMPLES, BEFORE EACH TEST CASE

	# @mock.patch.object(__builtin__, 'raw_input')
	# def setUp(self, mock_raw_input):
		# mock_raw_input.return_value = "00:00"
	
	def setUp(self):
		self.input1 = "00:00"
		self.input2 = "01:30"
		self.input3 = "12:05"
		self.input4 = "14:01"
		self.input5 = "21:00"
		self.inputs = ["00:00","01:30","12:05", "14:01", "21:00"]
		__builtin__.raw_input = mock.Mock(side_effect=self.inputs)
		self.ac1 = AlarmClock()
		self.ac2 = AlarmClock()
		self.ac3 = AlarmClock()
		self.ac4 = AlarmClock()
		self.ac5 = AlarmClock()
		

	def test_initial_alarm_clock(self):
		
		ac = self.ac1
		self.assertIsInstance(ac, AlarmClock)
		self.assertIsInstance(ac.alarm_time_str, str)
		self.assertIsInstance(ac.alarm_time_list, list)
		# print(ac.alarm_time_str)
		# ac = AlarmClock()
		# print(ac.alarm_time_str)
		# ac = AlarmClock()
		# print(ac.alarm_time_str)

	def test_get_alarm_time(self):
		# test string format:
		self.assertRegexpMatches(self.ac1.alarm_time_str, '([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]')

		#test all inputs received
		self.assertEqual(self.ac1.alarm_time_str, "00:00")
		self.assertEqual(self.ac2.alarm_time_str,"01:30")
		self.assertEqual(self.ac3.alarm_time_str,"12:05")
		self.assertEqual(self.ac4.alarm_time_str,"14:01")
		self.assertEqual(self.ac5.alarm_time_str,"21:00")

	def test_parse_alarm_time_str(self):
		# Case 00:00
		self.assertEqual(self.ac1.alarm_time_list, [0,0,0])
		# Case 01:30
		self.assertEqual(self.ac2.alarm_time_list, [1,3,0])
		# Case 12:05
		self.assertEqual(self.ac3.alarm_time_list, [12,0,5])
		# Case 14:01
		self.assertEqual(self.ac4.alarm_time_list, [14,0,1])
		# Case 21:00
		self.assertEqual(self.ac5.alarm_time_list, [21,0,0])

	def test_select_wav_files(self):
		# Case 00:00
		self.assertEqual(self.ac1.wav_list, ['./irishclock/its.wav', './irishclock/12.wav', './irishclock/am.wav'])
		# Case 01:30
		self.assertEqual(self.ac2.wav_list, ['./irishclock/its.wav', './irishclock/1.wav', './irishclock/30.wav', './irishclock/0.wav', './irishclock/am.wav'])
		# Case 12:05
		self.assertEqual(self.ac3.wav_list, ['./irishclock/its.wav', './irishclock/12.wav', './irishclock/o.wav', './irishclock/5.wav', './irishclock/pm.wav'])
		# Case 14:01
		self.assertEqual(self.ac4.wav_list, ['./irishclock/its.wav', './irishclock/2.wav', './irishclock/o.wav', './irishclock/1.wav', './irishclock/pm.wav'])
		# Case 21:00
		self.assertEqual(self.ac5.wav_list, ['./irishclock/its.wav', './irishclock/9.wav', './irishclock/pm.wav'])

	def test_determine_sleep_time(self):
		# Case 00:00
		self.assertEqual(self.ac1.sleep_time, 27060)
		# Case 01:30
		self.assertEqual(self.ac2.sleep_time, 32460)
		# Case 12:05
		self.assertEqual(self.ac3.sleep_time, 70560)
		# Case 14:01
		self.assertEqual(self.ac4.sleep_time, 77520)
		# Case 21:00
		self.assertEqual(self.ac5.sleep_time, 16260)

	def test_play_wav(self):
		# with self.assertRaises(IOError):
			# self.ac1.play_wav('non_existant_file.wav')
		# self.ac1.play_wav('./irishclock/pm.wav')
		# self.assertRaises(IOError,self.ac1.play_wav(),self.ac1, 'non_existant_file.wav')
		# self.assertEqual(self.ac1.play_wav('non_existant_file.wav'),"blahblah")

		# Test non existing file:
		capturedOutputError = StringIO.StringIO()
		capturedOutputPrint = StringIO.StringIO()
		
		sys.stderr = capturedOutputError
		sys.stdout = capturedOutputPrint
		
		self.ac1.play_wav('non_existant_file.wav')
		
		sys.stderr = sys.__stderr__
		sys.stdout = sys.__stdout__

		self.assertEqual(capturedOutputError.getvalue(), "IOError on file non_existant_file.wav\n[Errno 2] No such file or directory: 'non_existant_file.wav'. Skipping.\n")
		self.assertEqual(capturedOutputPrint.getvalue(), "Trying to play file non_existant_file.wav\n")


		# Test existing file:
		capturedOutputError = StringIO.StringIO()
		capturedOutputPrint = StringIO.StringIO()
		
		sys.stderr = capturedOutputError
		sys.stdout = capturedOutputPrint
		
		self.ac1.play_wav('./irishclock/pm.wav')
		
		sys.stderr = sys.__stderr__
		sys.stdout = sys.__stdout__

		self.assertEqual(capturedOutputError.getvalue(), "")
		self.assertEqual(capturedOutputPrint.getvalue(), "Trying to play file ./irishclock/pm.wav\n")



if __name__ == '__main__':
		unittest.main()