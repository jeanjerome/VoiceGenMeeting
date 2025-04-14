# 🎙️ VoiceGenMeeting

**VoiceGenMeeting** is a command-line tool that generates synthetic meeting audio from a simple text-based transcript, assigning a unique voice to each speaker. It's ideal for testing transcription, meeting analysis, or speech recognition tools.

## TTS Engine Versions

This project offers multiple implementations using different text-to-speech (TTS) engines. Choose the version that best suits your specific requirements:

### 1. Coqui-TTS Branch [`lib/coqui-tts`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/coqui-tts)
- **Recommended for**: Multilingual projects, especially non-English content
- **Strengths**: 
  - Exceptional phonetic accuracy across languages
  - Robust language support
- **Limitations**: Slightly monotonous intonation

### 2. Kokoro Branch [`lib/kokoro`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/kokoro)
- **Recommended for**: English-language projects
- **Strengths**:
  - Nuanced intonation
  - Expressive English speech synthesis
- **Limitations**: Poor handling of non-English phonetics

### 3. OuteTTS Branch [`lib/outetts`](https://github.com/jeanjerome/VoiceGenMeeting/tree/lib/outetts)
- **Based on**: Open-source TTS engine using llama.cpp and Transformers
- **Good for**: Experimental and lightweight use cases

## Choosing the Right Version

- **Multilingual Project**: Use Coqui-TTS branch
- **English-Only Project**: Use Kokoro branch
- **Experimental or Resource-Constrained Setup**: Use OuteTTS branch

We continuously evaluate and improve these implementations. Future versions may integrate the best features from each engine.

## Example Comparisons

Refer to the `example.wav` and `example_fr.wav` files in each branch to hear the differences in voice synthesis quality.

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

## License
[MIT](LICENSE)
