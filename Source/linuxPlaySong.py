import sys
import os
import time
import uinput

device = uinput.Device([	uinput.KEY_LEFTSHIFT,	
				uinput.KEY_LEFTBRACE,
				uinput.KEY_RIGHTBRACE,
				uinput.KEY_SEMICOLON,
				uinput.KEY_APOSTROPHE,
				uinput.KEY_GRAVE,
				uinput.KEY_BACKSLASH,
				uinput.KEY_COMMA,
				uinput.KEY_DOT,
				uinput.KEY_SLASH,
				uinput.KEY_MINUS,
				uinput.KEY_EQUAL,
				uinput.KEY_SLASH,

				uinput.KEY_1,
				uinput.KEY_2,
				uinput.KEY_3,
				uinput.KEY_4,
				uinput.KEY_5,
				uinput.KEY_6,
				uinput.KEY_7,
				uinput.KEY_8,
				uinput.KEY_9,
				uinput.KEY_0,

				uinput.KEY_A,
				uinput.KEY_B,
				uinput.KEY_C,
				uinput.KEY_D,
				uinput.KEY_F,
				uinput.KEY_E,
				uinput.KEY_G,
				uinput.KEY_H,
				uinput.KEY_I,
				uinput.KEY_J,
				uinput.KEY_K,
				uinput.KEY_L,
				uinput.KEY_M,
				uinput.KEY_N,
				uinput.KEY_O,
				uinput.KEY_P,
				uinput.KEY_Q,
				uinput.KEY_R,
				uinput.KEY_S,
				uinput.KEY_T,
				uinput.KEY_U,
				uinput.KEY_V,
				uinput.KEY_W,
				uinput.KEY_X,
				uinput.KEY_Y,
				uinput.KEY_Z])
keyOrder = "  1234567890-=  qwertyuiop[]  asdfghjkl;'` \\zxcvbnm,./"
shiftedKeyOrder = "  !@#$%^&*()_+  QWERTYUIOP{}  ASDFGHJKL:\"~ |ZXCVBNM<>?"

tstart = time.time()
isPlaying = False

	
def OnKeyDown(event):
	global isPlaying
	if(event.Key == "Delete"):
		isPlaying = not isPlaying
		if(isPlaying):
			runMacro()
	return True

def isShifted(charIn):
	asciiValue = ord(charIn)
	if(asciiValue >= 65 and asciiValue <= 90):
		return True
	if(charIn in "!@#$%^&*()_+{}|:\"<>?"):
		return True
	return False
	

def getKeyValue(charIn):
	asciiValue = ord(charIn)
	if(asciiValue >= 97 and asciiValue <= 122):
		return asciiValue - 32
	if((asciiValue >= 48 and asciiValue <= 57) or (asciiValue >= 65 and asciiValue <= 90)):
		return asciiValue
	if(charIn in ")!@#$%^&*("):
		return ")!@#$%^&*(".index(charIn) + 48
		

def pressLetter(charIn):
	if(charIn in keyOrder):
		device.emit_click((0x1,keyOrder.index(charIn)))
	elif(charIn in shiftedKeyOrder):
		device.emit_combo((uinput.KEY_LEFTSHIFT,(0x1,shiftedKeyOrder.index(charIn))))
	return
		
def processFile():
	with open("song.txt","r") as macro_file:
		lines = macro_file.read().split("\n")
		tOffsetSet = False
		tOffset = 0
		tempo = 60/float(lines[0].split(" ")[1])
		
		processedNotes = []
		
		for l in lines[1:]:
			l = l.split(" ")
			if(len(l) < 2):
				#print("INVALID LINE")
				continue
			
			waitToPress = float(l[0])
			notes = l[1]
			processedNotes.append([waitToPress,notes])
			if(not tOffsetSet):
				tOffset = waitToPress
				print("Starting macro with offset t=",tOffset)
				tOffsetSet = True
	return [tempo,tOffset,processedNotes]

def floorToZero(i):
	if(i > 0):
		return i
	else:
		return 0
	
def runMacro():
	global infoTuple
	tstart = time.time()
	for l in infoTuple[2]:
		goTime = (l[0] - infoTuple[1])*(infoTuple[0])
		if(goTime - (time.time() - tstart) > 0):
			time.sleep(floorToZero(goTime - (time.time() - tstart)))
		print("%10.2f %15s" % (l[0],l[1]))
		for n in l[1]:
			pressLetter(n)
infoTuple = processFile()
print("Processed File, waiting 5 seconds and then playing")
time.sleep(5)
runMacro()
