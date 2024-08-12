# MIDI to Virtual Piano Converter

Our partner application can be found over here: [MIDIPlusPlus](https://github.com/Zephkek/MIDIPlusPlus), featuring a ton of improvements and optimization.

Easily convert MIDI files into virtual piano sheet music for manual play or automated playback on platforms like [Virtual Piano](https://virtualpiano.net) and Roblox pianos.

## 🎹 Features

- **MIDI to Virtual Piano Sheet Conversion**: Quickly convert MIDI files into sheet music compatible with virtual pianos.
- **Automated and Manual Playback**: Choose between automated playback or manual control for playing the music.
- **Human-Like Playback with Legit Mode**: Simulate a human playing style with natural timing variations.
- **Playback Speed Control**: Adjust the playback speed to match your preference.
- **Auto Tempo Adjustment**: Automatically adjusts the tempo to suit the song.
- **Simple Setup**: Easy to install and run with minimal configuration.

## ⚠️ Important Information

This program uses the Python `pynput` library to simulate key presses. Some antivirus software may flag this as suspicious behavior. The executable files are created using `pyinstaller --onefile`, which bundles the Python program and its dependencies into a single, portable executable. You are encouraged to review the scripts and generate the executable yourself for added security.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed and added to your system PATH.

### Installation

1. **Download or Clone**: Visit the [releases page](https://github.com/Stereo101/python-MidiToVirtualPianoMacro/releases) and download the latest release for your operating system, or clone the repository:

    ```bash
    git clone https://github.com/Stereo101/python-MidiToVirtualPianoMacro
    ```

2. **Extract Files**: Extract the contents of `pyMIDI` and `playSong`. Add your MIDI files to the `midi` directory.

3. **Install Dependencies**: Open your terminal (Command Prompt for Windows, Terminal for macOS and Linux) and install the required Python library:

    ```bash
    pip install pynput
    ```

4. **Run the Program**:

   - Execute `pyMIDI` in your terminal. The program will list available songs from the `midi` directory.
   - Select a song to generate several files:
     - `song.txt`: The program reads this file to play the song.
     - `midiRecord.txt`: A debug log detailing the conversion process.
     - `SheetConversion.txt`: A human-readable version of `song.txt` displaying the notes in a more understandable format.
   - The program will wait for you to press the `Delete` key. Switch to your target application (e.g., Virtual Piano) and press `Delete` to start the automated playback.

## 📚 Tutorials and Demos

### Volcaniks' YouTube Guide
- [Watch the guide](https://www.youtube.com/watch?v=U1a6-y5X8BQ)

### Prizels' YouTube Guide
- [Watch the guide](https://www.youtube.com/watch?v=QsLP5m1MB3k)

### ⚠️ Shady Instruction Videos

These videos link to potentially unsafe third-party downloads. Proceed with caution:
- [Video 1](https://www.youtube.com/watch?v=wNDSCnH23eQ)
- [Video 2](https://www.youtube.com/watch?v=6kt07i82QlE)

## 💬 Join the Community

Need help or want to connect with others using the program? Join our [Discord server](https://discord.gg/Z4msASBqrR).
