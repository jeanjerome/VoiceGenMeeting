# 🎙️ VoiceGenMeeting

> **Note:** A more advanced version of this project is available on the `lib/kokoro` branch, utilizing the [Kokoro](https://github.com/hexgrad/kokoro) TTS engine. This version offers improved performance and enhanced text-to-speech capabilities. The [`lib/kokoro`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/kokoro) branch is planned to be merged into the main branch in the near future.
> 
> However, ongoing tests with various TTS engines are still underway to identify the absolute best text-to-speech solution, which could potentially lead to further significant improvements in the project.


**VoiceGenMeeting** is a command-line tool that generates synthetic meeting audio from a simple text-based transcript, assigning a unique voice to each speaker. It's ideal for testing transcription, meeting analysis, or speech recognition tools.

This project is powered by [**OuteTTS**](https://github.com/edwko/OuteTTS), an open-source text-to-speech engine built on top of llama.cpp and Transformers.


## Features

- Generates a `.wav` file from a `.txt` transcript formatted like:
  ```
  Marc : Hello, shall we begin?
  Julie : Yes, I'm ready.
  ```
- Automatically assigns a voice to each speaker
- Creates custom voice profiles from short audio files (`marc.mp3`, `julie.wav`, etc.)
- Saves and reuses speaker profiles from the `data/profiles` folder
- Converts and truncates source audio files to a maximum of 15 seconds
- Fully offline — no cloud API dependency thanks to OuteTTS


## Project Structure

```
VoiceGenMeeting/
├── conversation_tts.py       # Main CLI script
├── data/
│   ├── speakers/             # Raw speaker audio files (e.g. marc.mp3)
│   └── profiles/             # Generated speaker profiles (.json)
├── example*.txt              # Example transcript with multiple speakers
└── example*.wav              # Example result of generated audio output
```


## Installation

### Prerequisites
- Python 3.9+
- [ffmpeg](https://ffmpeg.org/) (required by `pydub` for audio conversion)

### Create a virtual environment (recommended)
Using conda:
```bash
conda create -n voicegen python=3.9 -y
conda activate voicegen
```

### Install Python dependencies
```bash
pip install pydub
```

### Platform-specific installation

#### On macOS (Apple Silicon or Intel)
```bash
brew install ffmpeg
CMAKE_ARGS="-DGGML_METAL=on" pip install outetts
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt install ffmpeg
pip install outetts
```

#### On Windows
- Download and install [ffmpeg](https://ffmpeg.org/download.html) and add it to your PATH
- Then install OuteTTS:
```bash
pip install outetts
```


## Usage

### 1. Prepare a `transcription.txt` file
```text
Marc : Good morning.
Julie : Ready to get started.
```

### 2. Add voice samples
Place short audio files in `data/speakers`, named after the speakers in your transcript (e.g. `marc.mp3`, `julie.wav`).

**Requirements for each file:**
- Audio format: `.mp3` or `.wav`
- Duration: ideally between 5 and 15 seconds (automatically truncated if longer)
- Content: clean voice, preferably with neutral tone, no background noise
- Channels: mono (or will be converted)
- Sample rate: 44.1 kHz (will be converted if needed)

Each file will be automatically converted to mono, 44.1kHz, and truncated to 15 seconds. to mono, 44.1kHz, and truncated to 15 seconds.

### 3. Generate audio
```bash
python conversation_tts.py transcription.txt output.wav
```


## Resources
- [OuteTTS on GitHub](https://github.com/edwko/OuteTTS)
- [HuggingFace TTS Models](https://huggingface.co/models?pipeline_tag=text-to-speech)


## License
[MIT](LICENSE)
