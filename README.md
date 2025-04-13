# 🎙️ VoiceGenMeeting

> ## TTS Engine Evaluation
>
> This project is available in multiple versions in different branches, each using a different text-to-speech engine:
> - [`lib/outetts`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/outetts) - Using [OuteTTS](https://github.com/edwko/OuteTTS), an open-source TTS engine based on llama.cpp and Transformers.
> - [`lib/kokoro`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/kokoro) - Using [Kokoro](https://github.com/hexgrad/kokoro), offering improved performance and enhanced TTS capabilities.
> - [`lib/coqui-tts`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/coqui-tts) - Using [Coqui-TTS](https://github.com/idiap/coqui-ai-TTS), the current main branch which delivers the best results to date (see example.wav and example_fr.wav files for comparison).
>
> ## Key Findings 
>
> Through comprehensive testing of various text-to-speech engines, we've identified nuanced performance characteristics:
> - `Coqui-TTS` demonstrates superior voice quality (phonetic accuracy) for non-English languages but lacks dynamic intonation.
> - The `Kokoro` TTS engine shows nuanced intonation for English content but struggles with non-English phonetic subtleties.
>
> Ongoing evaluation continues to refine our understanding of these technologies, with plans to integrate the most promising features from each engine in future iterations.

**VoiceGenMeeting** is a command-line tool that generates synthetic meeting audio from a simple text-based transcript, assigning a unique voice to each speaker. It's ideal for testing transcription, meeting analysis, or speech recognition tools.

This project is powered by [**Coqui TTS**](https://github.com/idiap/coqui-ai-TTS), an open-source text-to-speech engine maintained by Idiap Research Institute.

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
- Fully offline — no cloud API dependency thanks to Coqui TTS

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
- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (required by `pydub` for audio conversion)

### Create a virtual environment (recommended)
Using conda:
```bash
conda create -n voicegen python=3.10 -y
conda activate voicegen
```

### Install Python dependencies
```bash
pip install pydub soundfile numpy coqui-tts torch
```

### Platform-specific installation

#### On macOS (Apple Silicon or Intel)
```bash
brew install ffmpeg
pip install coqui-tts
```

#### On Linux (Ubuntu/Debian)
```bash
sudo apt install ffmpeg
pip install coqui-tts
```

#### On Windows
- Download and install [ffmpeg](https://ffmpeg.org/download.html) and add it to your PATH
- Then install Coqui TTS:
```bash
pip install coqui-tts
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
- Sample rate: any (will be automatically adapted)

Each file will be automatically converted to mono and truncated to 15 seconds. The sample rate will be handled according to the TTS model used (typically 22050 Hz for most TTS models).

### 3. Generate audio
```bash
python conversation_tts.py transcription.txt output.wav
```

You can also specify the language with an optional parameter:
```bash
python conversation_tts.py transcription.txt output.wav fr
```

## How It Works

VoiceGenMeeting uses multilingual speech synthesis and voice cloning technology to:

1. Analyze the conversation transcript line by line
2. Identify each speaker and assign them a voice based on their audio sample
3. Generate synthetic audio segments for each line of dialogue
4. Assemble all segments into a single audio file with natural pauses

The system primarily uses the XTTS v2 model (tts_models/multilingual/multi-dataset/xtts_v2) which offers:
- Support for over 17 languages
- High-fidelity voice cloning from a short sample
- Superior and natural sound quality

### Note on Sample Rate

Most speech synthesis models, including XTTS v2, use a sample rate of 22050 Hz (not 44100 Hz). The script automatically detects the correct sample rate from the model to avoid issues with high-pitched or too-fast playback that might occur when playing with an incorrect frequency.

## Resources
- [Coqui TTS on GitHub](https://github.com/idiap/coqui-ai-TTS)
- [Coqui TTS Documentation](https://coqui-tts.readthedocs.io/en/latest/)

## License
[MIT](LICENSE)