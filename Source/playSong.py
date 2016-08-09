import sys
import os
import time
import ctypes
from ctypes import wintypes
import pyHook
import pythoncom

stopPumping = False
user32 = ctypes.WinDLL('user32', use_last_error=True)
tstart = time.time()
isPlaying = False

	
def OnKeyDown(event):
	global isPlaying
	if(event.Key == "Delete"):
		isPlaying = not isPlaying
		if(isPlaying):
			runMacro()
	return True
	
INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

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
	kv = getKeyValue(charIn)
	if(isShifted(charIn)):
		PressKey(160)
		PressKey(kv)
		ReleaseKey(kv)
		ReleaseKey(160)
	else:
		PressKey(kv)
		ReleaseKey(kv)
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
	global isPlaying
	global infoTuple
	tstart = time.time()
	for l in infoTuple[2]:
		if(not isPlaying):
			break
		goTime = (l[0] - infoTuple[1])*(infoTuple[0])
		if(goTime - (time.time() - tstart) > 0):
			time.sleep(floorToZero(goTime - (time.time() - tstart)))
		print("%10.2f %15s" % (l[0],l[1]))
		for n in l[1]:
			pressLetter(n)
infoTuple = processFile()
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyDown
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()