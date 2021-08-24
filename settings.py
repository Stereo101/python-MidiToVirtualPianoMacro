import json
import os

#maps a string representing a note to a note index where C0 = 0
def note_to_index(note):
	note_offsets = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
	is_sharp = (note[1] == "#")
	note_letter = note[0]
	if is_sharp:
		note_number = int(note[2:])
	else:
		note_number = int(note[1:])
	index = 12 + note_offsets[note_letter] + int(is_sharp) + 12*note_number
	return index

#If alt_velocity is on, we need to calculate the velocity mapping
#	to keys in the key_binding_list.
def map_velocity(vel):
	index = int((int(vel)/128) * len(SETTINGS["key_binding_list"]))
	print("VEL INDEX",vel)
	return SETTINGS["key_binding_list"][index]
	
def apply_range_bounds(note_int):
	transpose = SETTINGS.get("transpose",0)
	note_int += transpose
	
	if note_int < SETTINGS["lowest_note"]:
		if SETTINGS["out_of_range_behavior"] == "skip":
			return None
		elif SETTINGS["out_of_range_behavior"] == "shift":
			while note_int < SETTINGS["lowest_note"]:
				note_int += 12
	
	elif note_int > SETTINGS["highest_note"]:
		if SETTINGS["out_of_range_behavior"] == "skip":
			return None
		elif SETTINGS["out_of_range_behavior"] == "shift":
			while note_int > SETTINGS["highest_note"]:
				note_int -= 12
	else:
		return note_int

def load():
	global SETTINGS
	settings_file = "settings.json"
	SETTINGS = json.load(open(settings_file,"r"))

	config_dir = SETTINGS["config_dir"]
	print("Config order is",SETTINGS["config_order"],"...")
	for config_file in SETTINGS["config_order"]:
		print(f"loading settings from '{config_file}'")
		config_path = os.path.join(config_dir,config_file)
		j = json.load(open(config_path,"r"))
		
		for k,v in j.items():
			SETTINGS[k] = v

	required_settings = ["key_binding_list","lowest_note"]
	if "key_binding_list" not in SETTINGS:
		print("'key_binding_list' must be defined")

	
		
	#Define list to convert value -> keypress
	key_map = [None] * 200
	index = note_to_index(SETTINGS["lowest_note"])
	SETTINGS["lowest_note"] = index
	for keys in SETTINGS["key_binding_list"]:
		key_map[index] = keys
		index += 1
	SETTINGS["key_map"] = key_map
	SETTINGS["highest_note"] = index-1
	
	if "warning" in SETTINGS:
		print(SETTINGS["warning"])
load()



