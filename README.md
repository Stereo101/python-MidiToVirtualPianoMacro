# PyMidi2VP

Python Midi To Virutal Piano is a tool for midi conversion for virtual piano playing across many virtual piano platforms.
The autoplayer generates keypresses that happen at the operating system level as to not require software hooks.

# Configure files
Configuration files specify which keys should be pressed for each note, and other options for specific virtual piano platforms.
These are written in [JSON or JavaScript Object Notation format](https://www.w3schools.com/js/js_json_intro.asp), and must adhere
to the standard to be properly loaded. Many platforms have niche settings that would ruin performance in for other platforms. These config 
files should work out of the box while users can still tune tolerances make make tweaks as they like.
If you have a platform you want supported, or options you wanted added, [open an issue here](https://github.com/Stereo101/python-MidiToVirtualPianoMacro/issues).

# Config Order
**settings.json** defines a **config_order** which loads these configure files in sequence.
Any individual setting can specified multiple times and only the last definition is used.
By default, the config sequence starts with **base.json** which has all required settings defined to get
the autoplayer working on most platforms. You should never have to edit **base.json**
as this will change behavior on all platforms. Instead edit the config specific to your platform
and add it to the settings sequence.

# Settings
name | description | valid values
-----|-------------|-------------
pause_key | Pauses and resumes playback on press | keycode
rewind_key | Rewinds playback on press | keycode
advance_key | Advances playback on press | keycode
lowest_note | Defines the value of the lowest note defined in 'key_binding_list'. | Note+Octave code ie "C0" or "A3"
key_binding_list | Defines an in order list from low to high of which keys to press. The first keycode in this list will be pressed when 'lowest_note' is played. | List of keycodes
key_instant_release | Release notes instantly instead of holding. Use for platforms that don't recognise hold behavior | true / false
playback_speed | Multiplies the speed at which playback occurs | any positive decimal. Include the 0 for values below 1 ie "0.8".
out_of_range_behavior | Decides whether notes outside the range are dropped or shifted into range | shift / skip
hold_to_play | press a key to advance the playback | true / false
hold_to_play_key | keycode used for tap_to_play | keycode
alt_velocity | Implemented for Roblox Piano Visualizations 2. Generates a alt+keycode press before each note to set velocity. | true / false
transpose | Shifts notes up or down. Effects autoplay and sheet music generation | postitive or negative integer
auto_next_song | __UNIMPLEMENTED__ Chooses a random song and starts playing once a song is over. | true / false

## About Keycodes
Keycodes are defined by the [python keyboard library](https://pypi.org/project/keyboard/).
Keypress events are interpretted by your operating system through scancodes values, and the keyboard library leverages the operating system
to make this conversion.

This runs into issues for different languages: "shift" will resolve to a valid scan code in an english locale, but
may not in a different locale. Please [open an issue](https://github.com/Stereo101/python-MidiToVirtualPianoMacro/issues) if 
you are using a non-english locale and think this error is happening to you.

## REPL
PyMidi2VP has a Read, Eval, Print, Loop (REPL) ui to make changing settings, processing songs, and playing songs happen in one place.
This needs a guide but is currently a WIP.
