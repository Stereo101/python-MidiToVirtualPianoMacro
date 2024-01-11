# to build, use "cd (playsong directory)"
# pyinstaller --onefile playSong.py

import keyboard
import subprocess
import threading

global isPlaying
global infoTuple
global storedIndex
global playback_speed
global elapsedTime

elapsedTime = 0

isPlaying = False
storedIndex = 0
conversionCases = {'!': '1', '@': '2', '£': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'}

key_delete = 'delete'
key_shift = 'shift'
key_end = 'end'
key_home = 'home'
key_load = 'f5'

def runPyMIDI():
    try:
        subprocess.run(["python", "pyMIDI.py"], check=True)
    except subprocess.CalledProcessError:
        print("pyMIDI.py was interrupted or encountered an error.")

def calculateTotalDuration(notes):
    total_duration = sum([note[0] for note in notes])
    return total_duration

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
		if strLetter in conversionCases:
			strLetter = conversionCases[strLetter]
		keyboard.release(strLetter.lower())
		keyboard.press(key_shift)
		keyboard.press(strLetter.lower())
		keyboard.release(key_shift)
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
    with open("song.txt", "r") as macro_file:
        lines = macro_file.read().split("\n")
        tOffsetSet = False
        tOffset = 0

        if len(lines) > 0 and "=" in lines[0]:
            try:
                playback_speed = float(lines[0].split("=")[1])
                print("Playback speed is set to %.2f" % playback_speed)
            except ValueError:
                print("Error: Invalid playback speed value")
                return None
        else:
            print("Error: Invalid playback speed format")
            return None

        tempo = None
        processedNotes = []
        
        for line in lines[1:]:
            if 'tempo' in line:
                try:
                    tempo = 60 / float(line.split("=")[1])
                except ValueError:
                    print("Error: Invalid tempo value")
                    return None
            else:
                l = line.split(" ")
                if len(l) < 2:
                    continue
                try:
                    waitToPress = float(l[0])
                    notes = l[1]
                    processedNotes.append([waitToPress, notes])
                    if not tOffsetSet:
                        tOffset = waitToPress
                        tOffsetSet = True
                except ValueError:
                    print("Error: Invalid note format")
                    continue

        if tempo is None:
            print("Error: Tempo not specified")
            return None

    return [tempo, tOffset, processedNotes]

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
    global isPlaying, storedIndex, playback_speed, elapsedTime

    notes = infoTuple[2]
    total_duration = calculateTotalDuration(notes)

    if isPlaying and storedIndex < len(notes):
        noteInfo = notes[storedIndex]
        delay = floorToZero(noteInfo[0])
        elapsedTime += delay

        # Process the notes for pressing or releasing
        if noteInfo[1][0] == "~":
            for n in noteInfo[1][1:]:
                releaseLetter(n)
        else:
            for n in noteInfo[1]:
                pressLetter(n)
        if "~" not in noteInfo[1]:
            elapsed_mins, elapsed_secs = divmod(elapsedTime, 60)
            total_mins, total_secs = divmod(total_duration, 60)
            print(f"[{int(elapsed_mins)}m {int(elapsed_secs)}s/{int(total_mins)}m {int(total_secs)}s] {noteInfo[1]}")

        storedIndex += 1
        if delay == 0:
            playNextNote()
        else:
            threading.Timer(delay/playback_speed, playNextNote).start()
    elif storedIndex >= len(notes):
        isPlaying = False
        storedIndex = 0
        elapsedTime = 0

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
	

	
	keyboard.on_press_key(key_delete, onDelPress)
	keyboard.on_press_key(key_home, rewind)
	keyboard.on_press_key(key_end, skip)
	keyboard.on_press_key(key_load, lambda _: runPyMIDI())
	
	print("\nControls")
	print("-" * 20)
	print("Press DELETE to play/pause")
	print("Press HOME to rewind")
	print("Press END to advance")
	print("Press F5 to load a new song")
	print("Press ESC to exit")

	while True:
		if keyboard.is_pressed('esc'):
			print("\nExiting...")
			break
			
if __name__ == "__main__":
	main()
