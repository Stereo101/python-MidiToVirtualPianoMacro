#lib imports
import keyboard
import threading
import time
import os
import re

import pyMIDI
import playSong

#local imports
from settings import SETTINGS

def repl():
	prompt = "\n> "
	commands = ["search","help","process","set","settings","exit","platform"]
	alias_map = 	{	"s":"search",
						"search":"search",
						"":"search",
						"set":"set",
						
						"?":"help",
						"help":"help",
						"h":"help",
						
						"process":"process",
						"p":"process",
						
						"platform":"platform",
						"plat":"platform",
						
						"settings":"settings",
						"options":"settings",
						"opts":"settings",
						
						"exit":"exit",
						"quit":"exit"
					}
	print("PyMidi REPL::")
	repl_help()	
	last_list_context = "search"
	song_list = []
	midi_list = []
	while True:
		cmd = input(prompt).strip()
		args = re.split(r"\s+",cmd)
		if len(args) == 0:
			continue
			
		if args[0].isnumeric():
			action = last_list_context
			args.append(0)
			for i in range(len(args)-1):
				args[i+1] = args[i]
		elif args[0] == "":
			action = last_list_context
		elif args[0].lower() not in alias_map:
			print(f"Unknown command '{args[0]}'. Type help or ?")
			continue
		else:
			action = alias_map[args[0].lower()]
		
		if action == "search":
			last_list_context = "search"
			song_dir = SETTINGS["song_dir"]
			
			if len(args) > 1 and args[1].isnumeric() and len(song_list) > 0:
				n = int(args[1])
				n = max(1,min(n,len(song_list)))
				song_choice = song_list[n-1]
				try:
					song_path = os.path.join(song_dir,song_choice)
					print("\n\n/////////////////////////////")
					print(f"Playing {song_choice} ...")
					playSong.mode_play(song_path)
				except KeyboardInterrupt as e:
					pass
				finally:
					keyboard.unhook_all()
					playSong.isPlaying = False
					playSong.storedIndex = 0
				repl_help()
			elif len(args) > 1:
				filter = " ".join(args[1:])
				song_choice,song_list = get_song_choice(song_dir,pass_input=1,filter=filter)
			else:
				song_choice,song_list = get_song_choice(song_dir,pass_input=1)
				
				
				
			
		
		elif action == "set":
			if len(args) < 3:
				print("Usage: set [SETTING] [VALUE]")
			else:
				k = args[1]
				v = " ".join(args[2:])
				
				if v.lower() == "true":
					print("bool val")
					v = True
				elif v.lower() == "false":
					print("bool val")
					v = False
				elif v.isnumeric():
					print("int val")
					v = int(v)
				elif re.match(r"[+-]?\d(>?\.\d+)?",v):
					print("float val")
					v = float(v)
				else:
					print("str val")
				SETTINGS[k] = v
				print(k,"=",v)
				
				
		elif action == "help":
			repl_help()
			
			
		elif action == "process":
			last_list_context = "process"
			midi_dir = SETTINGS["midi_dir"]
			
			if len(args) > 1 and len(midi_list) > 0:
				if args[1].isnumeric():
					n = int(args[1])
					n = max(1,min(n,len(midi_list)))
					midi_choice = midi_list[n-1]
					to_process = [midi_choice]
				elif args[1] == "all":
					to_process = midi_list
				
				for midi_choice in to_process:
					midi_path = os.path.join(midi_dir,midi_choice)
					midi = pyMIDI.MidiFile(midi_path)
					
					midi_first_name = midi_choice.split(".")[0]
					
					song_path = os.path.join(SETTINGS["song_dir"],midi_first_name + ".txt")
					sheet_path = os.path.join(SETTINGS["sheet_dir"],midi_first_name + ".txt")
					midi.save_song(song_path)
					midi.save_sheet(sheet_path)
				
				#repl_help()
				last_list_context = "search"
			else:
				midi_choice,midi_list = get_midi_choice(midi_dir,pass_input=1)
			
			
		elif action == "settings":
			for k,v in SETTINGS.items():
				if k not in ["key_map","key_binding_list","config_order","lowest_note","highest_note"] and "dir" not in k:
					print("%20s %20s" % (k,v))
		
		elif action == "platform":
			print("Not implemented, look in the config directory for current platform configurations.")
			print("Make a configuration default by editing 'settings.json'")
			print("To another config to load by default, add the config to the end of 'config_order' like this:",'\n\n"config_order":["base.json","roblox_piano_visualizations_2"]')
			print("\nPlease do not edit or remove 'base.json' which defines most needed settings")
		elif action == "exit":
			return
			
			
def repl_help():
	cmds = ["search","process","set","settings","exit","platform"]
	
	
	desc = {	"search":"list songs to play. alias: s",
				"platform":"list platform configuration files. alias: p,",
				"process":"convert midi files into VP sheets",
				"settings":"list current settings",
				"set":"temporarily change a setting",
				"exit":"quit the program"}
				
	examples = {	"search":["search bach"],
				"set":["set playback_speed 2.0"]}
	
	for c in cmds:
		print("\t",c)
		if c in desc:
			print("\t\t",desc[c])
		if c in examples:
			for ex in examples[c]:
				print("\t\t ex:",ex)
		print()

	
def get_song_choice(song_dir,pass_input=None,filter=None):
	#print("GET SONG CHOICE",pass_input,filter)
	fileList = os.listdir(song_dir)
	
	if len(fileList) == 0:
		print("There don't appear to be any songs here")
		print("you need to process midis before they are playable")
		return "",[]
	
	songList = []
	for f in fileList:
		if(".txt" in f or ".txt" in f.lower()):
			if filter is not None:
				if filter.lower() in f.lower():
					songList.append(f)
			else:
				songList.append(f)
	print("\nType the number of a song file then press enter:\n")
	for i in range(len(songList)):
		print(i+1,":",songList[i])

	if pass_input is not None:
		choice = pass_input
	else:
		choice = int(input(">"))
		
	choice_index = int(choice)
	
	if choice <= 0 or choice > len(songList):
		song_choice = ""
	else:
		song_choice = songList[choice_index-1]
	print()
	
	return song_choice,songList
	
def get_midi_choice(midi_dir,pass_input=None):
	fileList = os.listdir(midi_dir)
	midList = []
	
	if len(fileList) == 0:
		print("There are no midis in your midi directory")
		print(f"Your midi directory is currently set to '{midi_dir}'")
		return "",[]
	
	for f in fileList:
		if(".mid" in f or ".mid" in f.lower()):
			midList.append(f)
	print("\nType the number of a midi file press enter:\nType 'process all' to process all midis")
	for i in range(len(midList)):
		print(i+1,":",midList[i])
	if pass_input is not None:
		choice = pass_input
	else:
		choice = input(">").strip()
	print()
	
	if choice == "":
		return choice,midList
	else:
		choice_index = int(choice)
		return choice,midList

def main():
	repl()
	
if __name__ == "__main__":
	main()