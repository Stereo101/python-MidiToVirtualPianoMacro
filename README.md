# Midi to Virtual Piano
Generate virtual piano sheet music from a MIDI file also known as .mid files to play yourself or have your computer play it for you. Known to work well with [Virtual Piano](https://virtualpiano.net) and Roblox pianos.

# Discord
https://discord.gg/Z4msASBqrR

## Warning
This piano player portion of this program makes use of the python keyboard library which generates key presses programmatically. Antivirus software may (correctly) detect this as malicious activity! The executables were generated via `pyinstaller --onefile`, which bundles a python program and its dependencies into a portable executable that requires no setup. Everyone is welcome to audit the scripts and generate the executable for themselves. 

## Features

- **MIDI to Virtual Piano Sheet Conversion**: Convert MIDI files into sheet music for virtual pianos.
- **Automated and Manual Playback**: Play the music automatically or control playback manually.
- **Human-Like Playback with Legit Mode**: Simulate human playing style with timing variations.
- **Playback Speed Control**: Adjust the speed of the song playback as needed.
- **Easy Setup**: Simple to install and run.

## Instructions

`Make sure that python is installed and in PATH`

1. Go to the releases page and download the latest release for your operating system (Windows, Linux, etc.) or clone the repository using `git clone https://github.com/Stereo101/python-MidiToVirtualPianoMacro`.
2. Extract `pyMIDI` and `playSong` and add some MIDI files to the midi directory.
3. Install `pynput` by running `pip install pynput` in your terminal (Command Prompt for Windows. Terminal for MacOS and Linux.) 
4. Run `pyMIDI`. It will show you a list of songs from the midi directory. Pick any song and it will generate a few files.
   1. `song.txt` is what the program will read to play the song.
   2. `midiRecord.txt` is for debugging purposes. It is a log of what the converter did while processing the MIDI file.
   3. `SheetConversion.txt` is a human-readable version of `song.txt` that shows the notes in a more readable format.
5. It will wait for you to press the Delete key. Go to the program you want to play the song in and press the Delete key. The program will play the song for you.

It is not recommended to run `playsong` unless you know what you are doing.

## Tutorials and demos
### Volcaniks' youtube guide
https://www.youtube.com/watch?v=U1a6-y5X8BQ

### Prizels youtube guide
https://www.youtube.com/watch?v=QsLP5m1MB3k
	
## Shady Instruction videos
These videos link to *potentially* unsafe 3rd party downloads
```
https://www.youtube.com/watch?v=wNDSCnH23eQ
https://www.youtube.com/watch?v=6kt07i82QlE
```
