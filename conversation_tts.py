import sys
from pathlib import Path
from pydub import AudioSegment
import numpy as np
import soundfile as sf
from typing import Dict

# Import the updated Coqui TTS API
from TTS.api import TTS

# === Custom speaker profile management ===
def prepare_speaker_audio(name: str, speaker_dir: str = "data/speakers", max_duration_sec: int = 15):
    """Prepare speaker audio file by converting to WAV, mono, 44.1kHz and truncating if needed"""
    
    speaker_name = name.lower()
    # Check for both MP3 and WAV files
    mp3_path = Path(speaker_dir) / f"{speaker_name}.mp3"
    wav_path = Path(speaker_dir) / f"{speaker_name}.wav"
    
    input_path = mp3_path if mp3_path.exists() else wav_path
    
    if not input_path.exists():
        raise FileNotFoundError(f"[ERROR] Audio file not found for {name}: expected {mp3_path} or {wav_path}")

    print(f"[INFO] Processing {name}'s file: cutting and converting to WAV")

    # Convert to WAV (mono, 44.1 kHz, max duration)
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(44100)
    max_duration_ms = max_duration_sec * 1000
    if len(audio) > max_duration_ms:
        audio = audio[:max_duration_ms]

    # Export to processed WAV
    processed_wav_path = Path(speaker_dir) / f"{speaker_name}_processed.wav"
    audio.export(processed_wav_path, format="wav")
    
    print(f"[INFO] Audio processed for {name} → {processed_wav_path}")
    return str(processed_wav_path)

def generate_speech_for_line(tts: TTS, name: str, dialogue: str, 
                             speaker_files: Dict[str, str],
                             language: str = "en") -> np.ndarray:
    """Generate speech for a single line of dialogue"""
    
    if name not in speaker_files:
        print(f"[ERROR] No speaker file available for {name}")
        return np.array([])
    
    speaker_wav = speaker_files[name]
    
    try:
        # Generate speech using the current model
        # For XTTS or models that support voice cloning via speaker_wav
        if "xtts" in tts.model_name or tts.is_multi_speaker:
            audio = tts.tts(dialogue, speaker_wav=speaker_wav, language=language)
        # Fallback for other model types
        else:
            # Use voice conversion if the model doesn't natively support cloning
            temp_audio = tts.tts(dialogue)
            print(f"[INFO] Using voice conversion for {name}")
            audio = tts.voice_conversion(source_wav=temp_audio, target_wav=speaker_wav)
        
        # Get the actual sample rate from the model
        # This is crucial because TTS models might use different rates (22050 Hz is common)
        if hasattr(tts, "synthesizer") and hasattr(tts.synthesizer, "output_sample_rate"):
            original_sample_rate = tts.synthesizer.output_sample_rate
            print(f"[INFO] Model output sample rate: {original_sample_rate} Hz")
        else:
            # Default TTS sample rate if not available (many TTS models use 22050)
            original_sample_rate = 22050
            print(f"[INFO] Using default TTS sample rate: {original_sample_rate} Hz")
            
        return audio
    except Exception as e:
        print(f"[ERROR] Synthesis error for {name}: {e}")
        return np.array([])

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 conversation_tts.py <transcript_file.txt> [output_file.wav] [language_code]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.wav"
    language = sys.argv[3] if len(sys.argv) > 3 else "en"
    
    # Choose the TTS model - XTTS v2 is preferred for the best voice cloning
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    print(f"[INFO] Initializing Coqui TTS with model: {model_name}")
     # Get device (CUDA/MPS if available, otherwise CPU)
    if torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch, 'mps') and torch.backends.mps.is_available():
        device = "mps"  # For Apple Silicon Macs
    else:
        device = "cpu"
    
    print(f"[INFO] Using device: {device}")
    
    try:
        tts = TTS(model_name).to(device)
        print("[INFO] TTS model loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load model {model_name}: {e}")
        print("[INFO] Falling back to default model")
        tts = TTS().to(device)
    
    # Determine the correct sample rate from the model
    if hasattr(tts, "synthesizer") and hasattr(tts.synthesizer, "output_sample_rate"):
        sample_rate = tts.synthesizer.output_sample_rate
    else:
        # Many TTS models use 22050 Hz as the default sample rate
        sample_rate = 22050
    
    print(f"[INFO] Using sample rate: {sample_rate} Hz")
    
    speaker_files = {}
    audio_segments = []

    # First pass: prepare all speaker files
    seen_speakers = set()
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue

            name, dialogue = line.split(':', 1)
            name = name.strip()
            if not dialogue.strip():
                continue
                
            if name not in seen_speakers:
                seen_speakers.add(name)
                try:
                    # Prepare the speaker audio
                    processed_wav = prepare_speaker_audio(name)
                    speaker_files[name] = processed_wav
                except Exception as e:
                    print(f"[ERROR] Unable to process audio for {name}: {e}")

    # Second pass: generate speech for each line
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue

            name, dialogue = line.split(':', 1)
            name = name.strip()
            dialogue = dialogue.strip()
            if not dialogue:
                continue

            print(f"[INFO] Generating speech for {name}: '{dialogue}'")
            
            audio_data = generate_speech_for_line(tts, name, dialogue, speaker_files, language)
            
            if len(audio_data) > 0:
                # Add a pause between utterances
                pause = np.zeros(int(0.5 * sample_rate), dtype=np.float32)
                
                audio_segments.append(audio_data)
                audio_segments.append(pause)

    if audio_segments:
        # Concatenate all audio segments
        full_audio = np.concatenate(audio_segments)
        
        # Normalize audio to avoid clipping
        if np.max(np.abs(full_audio)) > 0.95:
            full_audio = 0.95 * full_audio / np.max(np.abs(full_audio))
            
        # Use the appropriate sample rate for writing the output file
        print(f"[INFO] Writing output with sample rate: {sample_rate} Hz")
        sf.write(output_path, full_audio, sample_rate)
        print(f"\n✅ Audio generated successfully: {output_path}")
    else:
        print("\n⚠️ No audio segments generated. Check your text file content and available profiles.")

if __name__ == "__main__":
    import torch  # Import torch here to avoid import errors if not available
    main()