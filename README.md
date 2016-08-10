WARNING:	
	THIS PROGRAM USES PYHOOK AND CTYPES TO HOOK INTO WINDOWS TO LISTEN FOR KEYPRESSES OR EXECUTE THEM, EVEN WHEN THE PROGRAM IS RUNNING BUT NOT IN FOCUS.
	
	THAT MAY SET OFF ANTIVIRUS SOFTWARE (as it should thats a fairly shady thing to do).
	
	I DO NOT RECCOMEND LEAVING THE PLAYER RUNNING WHILE TYPING ANY PASSWORDS/CREDITCARD#'S ETC
	
	I DO NOT KNOW ENOUGH ABOUT PYHOOK OR CTYPES TO GAURENTEE IT WILL NOT LEAK THESE KEYPRESSES TO OTHER PROGRAMS, OR PRESENT SOME SORT OF VULNERABILITY
	
	THE SOURCE CODE IS AVAILIABLE AND IS COMPILED INTO AN EXE FILE USING PYINSTALLER --ONEFILE
	
	IF YOU DO NOT TRUST THE EXE'S, YOU CAN RUN THE PYTHON SCRIPTS DIRECTLY WITH THE CORRECT LIBRARIES
	INSTALLED(PYHOOK,WINTYPES,PYTHONCOM) basically all the stuff in the playSong.py import block
	
	I INCLUDED THE EXE'S BECAUSE THEY ARE A CONVIENIENT WAY TO GET THE PROJECT WORKING WITH NO INSTALLATION/LIBRARIES REQUIRED.
	

Instructions:

	Place a .mid file in this directory and run pyMIDI.exe to process it. <Press the corresponding key and blah blah blah>
		IT WILL ONLY SEE FILES THAT CONTAIN .MID IN THE NAME, preferrably at the end, but not limited to
		
	This will generate a song.txt file and a midiRecord.txt file.
	
	The midiRecord is used for debugging and is a log of what the program did with the midi.
	
	The song.txt file is what is played by playSong.exe
	
	To play the Song, start playSong.exe, a black box will appear, nothing will happen until you hit the DELETE key
	
	Make sure you have virtualPiano in focus before pressing DELETE, or it will just start pressing the keys at whatever
	you have selected and is annoyingly difficult to stop
	
	Pressing DELETE a second time stops the song execution, but may not work at the beginning of the song for some reason.
	(ctypes/PyHook may be holding up the input buffer?)
	
	This does not close the program however, so pressing DELETE a third time would start the playing again from the
	beginning

In case you wanted to manually edit the song.txt file heres a breakdown:

	The song file has 2 elements, tempo and notes
	
	The tempo goes on the first line, and work like you would expect
	
	The notes have a timing portion, and an execution portion
	
	The program will stop playing until the time passed is > the note timing
	
	eg. if you have notes
	
		20 b
		
		25 c
		
		20 d
		
	The time will start at t=20, and immediately b will play, 5 beats will pass, then c AND d will be played at the same time
	
	You can also place notes in clusters and all will be played at the same time aswell.
	
		20 hjk
		
		21 ajl*
		
		...
		

	playSong.exe uses ctypes to execute the keypress as they appear
	
	
IMPORTANT: 	The tempo defaults to 120 unless a tempo meta event occurs within the midifile.

			The song's original tempo may not be the correct one to put in the song.txt file (It was for all my trials but I imagine this will not always be the case)
			
			For some songs the tempo is changed midsong many times over, and nothing is in place to account for that, so the last tempo recorded is the tempo it pulls from the midi and puts at the top of song.txt.
			
			
Note: This program did work with a multiple instrument midi file, but gave very confusing results.

	  I really reccomend using piano only midi files, or the result will be completely garbage
	  
THINGS TO ADD:

	START/END tags in the song.txt to make them easier to edit and playback specific portions
	
	Better midi file processing, it is fairly barebones right now, Only listens for note on (0x9N, where N represents the channel in hex) messages with to get note presses
		All other codes are read and basically ignored except for how big they are so I can advance through the file on track
		
	Pull tempo from the midi file correctly
	
	Change keypresses from global to focused to the virtual piano window (Anyone could really write a seperate song.txt interpreter to get the keypresses to the virtualPiano, Maybe even as a browser extension)
	
		The current solution is limited in scope to Windows Operating Systems and really shouldn't have to be
		
