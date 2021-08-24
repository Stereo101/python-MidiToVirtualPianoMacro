# to build, use "cd (playsong directory)"
# pyinstaller --onefile playSong.py

#lib imports
import keyboard
import threading
import time
import os
import re

#local imports
from settings import SETTINGS,map_velocity,apply_range_bounds

global isPlaying
global midi_action_list


isPlaying = False
storedIndex = 0
conversionCases = {'!': '1', '@': '2', '£': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'}

"""
#maps a string representing a note to a note index where C0 = 0
note_offsets = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def note_to_index(note):
	is_sharp = (note[1] == "#")
	note_letter = note[0]
	if is_sharp:
		note_number = int(note[2:])
	else:
		note_number = int(note[1:])
	index = note_offsets[note_letter] + int(is_sharp) + 12*note_number
	return index
	
octave_note_order = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def index_to_note(index):
	base_letter = "A"
	base_octave = 0
	val = 21
	#A0 is value 21 in midi
	octave = (index - 12) // 12
	letter = (index - 12) % 12
	return octave_note_order[letter] + str(octave)
"""

def onDelPress(event):
	global isPlaying
	isPlaying = not isPlaying

	if isPlaying:
		print("Playing...")
		playNextNote()
	else:
		print("Stopping...")

	return True

def isShifted(charIn):
	#print(charIn)
	if "shift" in charIn:
		return True
	asciiValue = ord(charIn)
	if(asciiValue >= 65 and asciiValue <= 90):
		return True
	if(charIn in "!@#$%^&*()_+{}|:\"<>?"):
		return True
	return False

def pressLetter(strLetter):
	if isShifted(strLetter):
		# we have to convert all symbols to numbers
		if strLetter in conversionCases:
			strLetter = conversionCases[strLetter]
		keyboard.release(strLetter.lower())
		
		keyboard.press("shift")
		keyboard.press(strLetter.lower())
		keyboard.release("shift")
		if SETTINGS.get("key_instant_release") == True:
			keyboard.release(strLetter.lower())
		
	else:
		keyboard.release(strLetter)
		keyboard.press(strLetter)
		
		if SETTINGS.get("key_instant_release") == True:
			keyboard.release(strLetter)
	return
	
def releaseLetter(strLetter):
	if isShifted(strLetter):
		if strLetter in conversionCases:
				strLetter = conversionCases[strLetter]
		keyboard.release(strLetter.lower())
	else:
		keyboard.release(strLetter)
	return

#Mini class to organize different actions into standard chunks
class Midi_Action:
	def __init__(self,offset,note_list,velocity,tempo_change):
		self.tempo_change = tempo_change
		self.note_list = note_list
		self.velocity = velocity
		self.offset = offset

def processFile(song_path):
	global playback_speed
	with open(song_path,"r") as macro_file:
		lines = macro_file.read().split("\n")
		processed_notes = []
		
		for line in lines:
			if len(line.strip()) == 0:
				continue
		
			try:
				#print(line)
				offset,note_str = line.split(" ",1)
				note_group,velocity = note_str.split(":")
				if "tempo" in note_str:
					tempo_change = int(note_group.split("tempo=")[1])
					note_list = []
				else:
					tempo_change = None
				
					note_list = note_group.split(" ")
					new_note_list = []
					for n in note_list:
						v = apply_range_bounds(int(n))
						if v is not None:
							new_note_list.append(SETTINGS["key_map"][v])
					note_list = new_note_list
					#print(note_list)
					#input()
				
				m = Midi_Action(	float(offset),
									note_list,
									int(velocity),
									tempo_change)
				processed_notes.append(m)
			except Exception as e:
				print(f"Error reading line:: '{line}'")
				print(e)
				input()

	return processed_notes

# for this method, we instead use delays as l[0] and work using indexes with delays instead of time
# we'll use recursion and threading to press keys
def set_note_offsets(midi_action_list):
	# parse time between each note
	# while loop is required because we are editing the array as we go
	i = 0
	while i < len(midi_action_list)-1:
		note = midi_action_list[i]
		nextNote = midi_action_list[i+1]
		if note.tempo_change:
			tempo = 60/float(note.tempo_change)
			midi_action_list.pop(i)

			note = midi_action_list[i]
			if i < len(midi_action_list)-1:
				nextNote = midi_action_list[i+1]
		else:
			note.offset = (nextNote.offset - note.offset) * tempo
			i += 1

	# let's just hold the last note for 1 second because we have no data on it
	midi_action_list[-1].offset = 1.00

	return midi_action_list

def playNextNote():
	global isPlaying
	global storedIndex
	global playback_speed

	while isPlaying and storedIndex < len(midi_action_list):
		note = midi_action_list[storedIndex]
		delay = max(note.offset,0)

		if note.velocity == 0:
			#release notes
			for n in note.note_list:
				releaseLetter(n)
		else:
			#press notes
			if SETTINGS.get("alt_velocity",False) == True:
				vel_key = map_velocity(note.velocity)
				print("alt+",vel_key)
				keyboard.press("alt")
				keyboard.press_and_release(vel_key)
				keyboard.release("alt")
			
			if SETTINGS.get("hold_to_play",False) == True:
				while not keyboard.is_pressed(SETTINGS.get("hold_to_play_key")):
					time.sleep(.05)
			
			for n in note.note_list:
				pressLetter(n)
		if(note.tempo_change is None and note.velocity != 0):
			print("%10.2f %15s %d" % (delay,"".join(note.note_list),note.velocity))
		#print("%10.2f %15s" % (delay/playback_speed,noteInfo[1]))
		storedIndex += 1
		if(delay != 0):
			threading.Timer(delay/playback_speed, playNextNote).start()
			return
	if storedIndex > len(midi_action_list)-1:
		isPlaying = False
		storedIndex = 0
	return

#TODO (BUG)
#Rewind and Fast Forward skip over tempo events
#	missing a critical tempo event will change playback significantly.
def rewind(KeyboardEvent):
	global storedIndex
	if storedIndex - 10 < 0:
		storedIndex = 0
	else:
		storedIndex -= 10
				
	print("Rewound to %.2f" % storedIndex)

def skip(KeyboardEvent):
	global storedIndex
	if storedIndex + 10 > len(midi_action_list):
		isPlaying = False
		storedIndex = 0
	else:
		storedIndex += 10
	print("Skipped to %.2f" % storedIndex)


def get_file_choice(song_dir):
	fileList = os.listdir(song_dir)
	songList = []
	for f in fileList:
		if(".txt" in f or ".txt" in f.lower()):
			songList.append(f)
	print("\nType the number of a song file then press enter:\n")
	for i in range(len(songList)):
		print(i+1,":",songList[i])

	choice = int(input(">"))
	print()
	choice_index = int(choice)
	return songList[choice_index-1],songList

def mode_play(song_path):
	global isPlaying
	global midi_action_list
	global playback_speed
	
	playback_speed = SETTINGS["playback_speed"]
	isPlaying = False
	storedIndex = 0
	
	midi_action_list = processFile(song_path)
	set_note_offsets(midi_action_list)
	
	keyboard.on_press_key(SETTINGS["pause_key"], onDelPress)
	keyboard.on_press_key(SETTINGS["rewind_key"], rewind)
	keyboard.on_press_key(SETTINGS["advance_key"], skip)
	
	print()
	print("Controls")
	print("-"*20)
	print(f"Press {SETTINGS['pause_key'].upper()} to play/pause")
	print(f"Press {SETTINGS['rewind_key'].upper()} to rewind")
	print(f"Press {SETTINGS['advance_key'].upper()} to advance")
	if SETTINGS.get("hold_to_play",False) == True:
		print(f"Hold {SETTINGS['hold_to_play_key'].upper()} while song is unpaused to play notes")
	while True:
		input("Press Ctrl+C to go back\n\n")

def main():
	song_dir = SETTINGS["song_dir"]
	
	
	while True:
		song_choice,_ = get_file_choice(song_dir)
		song_path = os.path.join(song_dir,song_choice)
		try:
			mode_play(song_path)
		except KeyboardInterrupt as e:
			pass
		finally:
			keyboard.unhook_all()
			storedIndex = 0
			isPlaying = False
	
	
		
if __name__ == "__main__":
	main()
