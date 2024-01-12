# Midi to Virtual Piano
Generate virtual piano sheet music from a MIDI file to play yourself or have your computer play it for you. Known to work well with [Virtual Piano](https://virtualpiano.net) and Roblox multiplayer pianos.

## Warning
This piano player portion of this program makes use of the python keyboard library which generates key presses programmatically. Antivirus software may (correctly) detect this as malicious activity! The executable were generated through a `pyinstaller --onefile`, which bundles a python program and its dependencies into a portable executable that requires no setup. Everyone is welcome to audit the source files and generate the executable for themselves. 

## Features

- **MIDI to Virtual Piano Sheet Conversion**: Convert MIDI files into sheet music for virtual pianos.
- **Automated and Manual Playback**: Play the music automatically or control playback manually.
- **Human-Like Playback with Legit Mode**: Simulate human playing style with timing variations.
- **Playback Speed Control**: Adjust the speed of the song playback as needed.
- **Easy Setup**: Simple to install and run.

## Instructions
1. Go to the releases page and download the latest release for your operating system (Windows, Linux, etc.).
2. Extract `pyMIDI` and `playSong` and add some MIDI files to the same directory as the two programs.
3. In the folder's address bar, type cmd and press Enter. This opens the Command Prompt in that folder. Then, type `pip install pynput` to install the required python package.
4. Run `pyMIDI`. It will show you a list of songs from the directory it is in. Pick any song and it will generate a few files.
   1. `song.txt` is that `playSong` will read to play the song.
   2. `midiRecord.txt` is for debugging purposes. It shows that the converter did while converting the MIDI file.
   3. `SheetConversion.txt` is a human-readable version of `song.txt` that shows the notes in a more readable format.
5. Run `playSong`. It will wait for you to press the Delete key. Go to the program you want to play the song in and press the Delete key. The program will play the song for you.

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
