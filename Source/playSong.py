# to build, use "cd (playsong directory)"
# pyinstaller --onefile playSong.py

import keyboard
import threading

global isPlaying
global infoTuple

isPlaying = False
storedIndex = 0
conversionCases = {'!': '1', '@': '2', '£': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'}

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
		keyboard.press('left shift')
		keyboard.press(strLetter.lower())
		keyboard.release('left shift')
	else:
		keyboard.release(strLetter)
		keyboard.press(strLetter)
	return
	
def releaseLetter(strLetter):
	if isShifted(strLetter):
		if strLetter in conversionCases:
				strLetter = conversionCases[strLetter]
		keyboard.release(strLetter.lower())
	else:
		keyboard.release(strLetter)
	return
	
def processFile():
	global playback_speed
	with open("song.txt","r") as macro_file:
		lines = macro_file.read().split("\n")
		tOffsetSet = False
		tOffset = 0
		playback_speed = float(lines[0].split("=")[1])
		print("Playback speed is set to %.2f" % playback_speed)
		tempo = 60/float(lines[1].split("=")[1])
		
		processedNotes = []
		
		for l in lines[1:]:
			l = l.split(" ")
			if(len(l) < 2):
				# print("INVALID LINE")
				continue
			
			waitToPress = float(l[0])
			notes = l[1]
			processedNotes.append([waitToPress,notes])
			if(not tOffsetSet):
				tOffset = waitToPress
				print("Start time offset =",tOffset)
				tOffsetSet = True

	return [tempo,tOffset,processedNotes]

def floorToZero(i):
	if(i > 0):
		return i
	else:
		return 0

# for this method, we instead use delays as l[0] and work using indexes with delays instead of time
# we'll use recursion and threading to press keys
def parseInfo():
	
	tempo = infoTuple[0]
	notes = infoTuple[2][1:]
	
	# parse time between each note
	# while loop is required because we are editing the array as we go
	i = 0
	while i < len(notes)-1:
		note = notes[i]
		nextNote = notes[i+1]
		if "tempo" in note[1]:
			tempo = 60/float(note[1].split("=")[1])
			notes.pop(i)

			note = notes[i]
			if i < len(notes)-1:
				nextNote = notes[i+1]
		else:
			note[0] = (nextNote[0] - note[0]) * tempo
			i += 1

	# let's just hold the last note for 1 second because we have no data on it
	notes[len(notes)-1][0] = 1.00

	return notes

def playNextNote():
	global isPlaying
	global storedIndex
	global playback_speed

	notes = infoTuple[2]
	if isPlaying and storedIndex < len(infoTuple[2]):
		noteInfo = notes[storedIndex]
		delay = floorToZero(noteInfo[0])

		if noteInfo[1][0] == "~":
			#release notes
			for n in noteInfo[1][1:]:
				releaseLetter(n)
		else:
			#press notes
			for n in noteInfo[1]:
				pressLetter(n)
		if("~" not in noteInfo[1]):
			print("%10.2f %15s" % (delay,noteInfo[1]))
		#print("%10.2f %15s" % (delay/playback_speed,noteInfo[1]))
		storedIndex += 1
		if(delay == 0):
			playNextNote()
		else:
			threading.Timer(delay/playback_speed, playNextNote).start()
	elif storedIndex > len(infoTuple[2])-1:
		isPlaying = False
		storedIndex = 0

def rewind(KeyboardEvent):
	global storedIndex
	if storedIndex - 10 < 0:
		storedIndex = 0
		
	else:
		storedIndex -= 10
	print("Rewound to %.2f" % storedIndex)

def skip(KeyboardEvent):
	global storedIndex
	if storedIndex + 10 > len(infoTuple[2]):
		isPlaying = False
		storedIndex = 0
	else:
		storedIndex += 10
	print("Skipped to %.2f" % storedIndex)


def main():
	global isPlaying
	global infoTuple
	global playback_speed
	infoTuple = processFile()
	infoTuple[2] = parseInfo()
	keyboard.on_press_key("delete", onDelPress)
	keyboard.on_press_key("home", rewind)
	keyboard.on_press_key("end", skip)
	
	print()
	print("Controls")
	print("-"*20)
	print("Press DELETE to play/pause")
	print("Press HOME to rewind")
	print("Press END to advance")
	while True:
		input("Press Ctrl+C or close window to exit\n\n")
		
if __name__ == "__main__":
	main()