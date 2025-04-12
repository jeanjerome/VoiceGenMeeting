# 🎙️ VoiceGenMeeting

**VoiceGenMeeting** is a command-line tool that generates synthetic meeting audio from a simple text-based transcript, assigning a unique voice to each speaker. It's ideal for testing transcription, meeting analysis, or speech recognition tools.

This project is powered by [**Kokoro**](https://huggingface.co/hexgrad/Kokoro-82M), an open-weight text-to-speech model with 82 million parameters, delivering high-quality and efficient synthetic voices.

## Features

- Generates a `.wav` file from a `.txt` transcript formatted like:
  ```
  Marc : Hello, shall we begin?
  Julie : Yes, I'm ready.
  ```
- Automatically assigns a unique voice to each speaker
- Supports multiple languages (American English, British English, Spanish, French, Hindi, Italian, Brazilian Portuguese, Japanese, Mandarin Chinese)
- Uses Kokoro's lightweight and efficient TTS model
- Fully customizable voice selection
- Offline TTS generation

## Project Structure

```
VoiceGenMeeting/
├── conversation_tts.py       # Main CLI script
├── data/
│   ├── speakers/             # Raw speaker audio files (optional)
│   └── profiles/             # Generated speaker profiles (optional)
├── example*.txt              # Example transcript with multiple speakers
└── example*.wav              # Example result of generated audio output
```

## Installation

### Prerequisites
- Python 3.9+
- [espeak-ng](https://github.com/espeak-ng/espeak-ng) (required by Kokoro)

### Create a virtual environment (recommended)
Using conda:
```bash
conda create -n voicegen python=3.9 -y
conda activate voicegen
```

### Install Python dependencies
```bash
pip install kokoro soundfile
```

### Platform-specific installation

#### On macOS (Apple Silicon)
```bash
pip install kokoro
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

#### On Linux
```bash
sudo apt-get install espeak-ng
pip install kokoro misaki[en]
```

#### On Windows
1. Install [espeak-ng](https://github.com/espeak-ng/espeak-ng/releases)
2. Install Kokoro:
```bash
pip install kokoro
```

## Usage

### 1. Prepare a `transcription.txt` file
```text
Marc : Good morning.
Julie : Ready to get started.
```

### 2. Generate audio
```bash
# For American English
python conversation_tts.py a transcription.txt output.wav

# For other languages, change the language code:
# a: American English (default)
# b: British English
# e: Spanish
# f: French
# h: Hindi
# i: Italian
# p: Brazilian Portuguese
# j: Japanese
# z: Mandarin Chinese
```

### Voice Customization
You can customize voice assignments in the `conversation_tts.py` script by modifying the `voice_mapping` dictionary or the `get_voice_for_speaker()` function.

Available Kokoro voices include:
- Female voices: `af_heart`, `af_bella`, `af_nicole`, `af_kore`, `af_aoede`, `af_sarah`
- Male voices: `am_michael`, `am_fenrir`, `am_echo`, `am_eric`, `am_puck`

## Resources
- [Kokoro TTS Model](https://huggingface.co/hexgrad/Kokoro-82M)
- [Kokoro Documentation](https://pypi.org/project/kokoro/)
- [Misaki G2P Library](https://github.com/hexgrad/misaki)

## Performance
Kokoro offers:
- 82 million parameters
- Comparable quality to larger models
- Significantly faster inference
- Lower computational cost
- Apache-licensed weights

## License
[MIT](LICENSE)