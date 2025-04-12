#!/usr/bin/env python3
import sys
import numpy as np
import soundfile as sf
from kokoro import KModel, KPipeline

# === Kokoro Voice Profile Management ===
def get_voice_for_speaker(name: str, voice_mapping=None):
    """
    Get appropriate Kokoro voice for a given speaker.
    Uses either a defined mapping or assigns a default voice.
    
    Args:
        name: Speaker's name
        voice_mapping: Optional dictionary of {name: kokoro_voice} mappings
    
    Returns:
        A string containing Kokoro voice identifier
    """
    # Default voices, organized by gender for easier assignment
    female_voices = ['af_heart', 'af_bella', 'af_nicole', 'af_kore', 'af_aoede', 'af_sarah']
    male_voices = ['am_michael', 'am_fenrir', 'am_echo', 'am_eric', 'am_puck']
    
    # If an explicit mapping exists, use it
    if voice_mapping and name in voice_mapping:
        return voice_mapping[name]
    
    # Otherwise, assign a voice deterministically based on the name
    # to always get the same voice for the same speaker
    name_hash = sum(ord(c) for c in name)
    if name.lower().endswith(('a', 'e', 'i')):  # Very simple gender heuristic
        voice = female_voices[name_hash % len(female_voices)]
    else:
        voice = male_voices[name_hash % len(male_voices)]
    
    print(f"[INFO] Assigning voice {voice} to {name}")
    return voice

# === Main Script ===
def main():
    if len(sys.argv) < 3:
        print("Usage: python conversation_tts.py <language_code> <transcript_file.txt> [output_file.wav]")
        print("Language codes:")
        print("  a: American English")
        print("  b: British English")
        print("  e: Spanish")
        print("  f: French")
        print("  h: Hindi")
        print("  i: Italian")
        print("  p: Brazilian Portuguese")
        print("  j: Japanese")
        print("  z: Mandarin Chinese")
        sys.exit(1)

    lang_code = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output.wav"
    
    # Custom name -> Kokoro voice mapping 
    # You can modify this section to assign specific voices
    voice_mapping = {
        # Example: "Jean": "am_michael",
        # "Marie": "af_heart",
    }
    
    # Initialize Kokoro model once for entire execution
    model = KModel().eval()
    
    # Dictionary to store pipelines by language
    pipelines = {
        lang_code: KPipeline(lang_code=lang_code, model=model)
    }
    
    # Fallback to American English if language-specific pipeline fails
    default_pipeline = KPipeline(lang_code='a', model=model)
    
    sample_rate = 24000  # Kokoro uses 24kHz sampling rate
    audio_segments = []

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

            # Use a default voice mapping if not specified
            if not voice_mapping:
                voice = get_voice_for_speaker(name)
            else:
                voice = voice_mapping.get(name, get_voice_for_speaker(name))
            
            # Use the specified language pipeline, with fallback
            pipeline = pipelines.get(lang_code, default_pipeline)
            
            try:
                # Generate audio with Kokoro
                print(f"[INFO] Generating audio for {name} with voice {voice}: {dialogue[:50]}...")
                
                # Get the first audio segment generated
                for segment in pipeline(dialogue, voice=voice, speed=1.0):
                    if segment.audio is not None:
                        audio_data = segment.audio.numpy()
                        
                        # Add audio segment followed by a pause
                        audio_segments.append(audio_data)
                        
                        # Add 0.5 second pause
                        pause = np.zeros(int(0.5 * sample_rate))
                        audio_segments.append(pause)
                        break  # We take only the first segment
            
            except Exception as e:
                print(f"[ERROR] Synthesis error for {name}: {e}")
                continue

    if audio_segments:
        full_audio = np.concatenate(audio_segments)
        sf.write(output_path, full_audio, sample_rate)
        print(f"\n✅ Audio generated successfully: {output_path}")
    else:
        print("\n⚠️ No audio segments generated. Check your transcript file.")

if __name__ == "__main__":
    main()