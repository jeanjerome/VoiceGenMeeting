import sys
import random
import os
import io
from pathlib import Path
from pydub import AudioSegment

import outetts
import soundfile as sf
import numpy as np

# === Gestion des profils de locuteur personnalisés ===
def get_or_create_speaker_profile(name: str, interface: outetts.Interface,
                                   speaker_dir: str = "data/speakers",
                                   profile_dir: str = "data/profiles"):
    speaker_name = name.lower()
    input_path = Path(speaker_dir) / f"{speaker_name}.mp3"
    profile_path = Path(profile_dir) / f"{speaker_name}.json"

    if profile_path.exists():
        print(f"[INFO] Chargement du profil existant pour {name}")
        return interface.load_speaker(str(profile_path))

    if not input_path.exists():
        raise FileNotFoundError(f"[ERREUR] Fichier audio introuvable pour {name} : {input_path}")

    print(f"[INFO] Traitement du fichier de {name} : découpe et conversion en WAV")

    # Convertir le MP3 en WAV (mono, 44.1 kHz, max 20s)
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(44100)
    max_duration_ms = 15 * 1000
    if len(audio) > max_duration_ms:
        audio = audio[:max_duration_ms]

    # Exporter en WAV temporaire
    tmp_wav_path = Path(speaker_dir) / f"{speaker_name}_processed.wav"
    audio.export(tmp_wav_path, format="wav")

    # Entraîner le profil depuis le WAV temporaire
    speaker = interface.create_speaker(str(tmp_wav_path))
    os.makedirs(profile_dir, exist_ok=True)
    interface.save_speaker(speaker, str(profile_path))

    print(f"[INFO] Profil enregistré pour {name} → {profile_path}")
    return speaker

# === Script principal ===
def main():
    if len(sys.argv) < 2:
        print("Utilisation : python3 conversation_tts.py <fichier_transcription.txt> [fichier_sortie.wav]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.wav"

    interface = outetts.Interface(config=outetts.ModelConfig.auto_config(
        model=outetts.Models.VERSION_1_0_SIZE_1B,
        backend=outetts.Backend.LLAMACPP,
        quantization=outetts.LlamaCppQuantization.FP16
    ))

    voice_map = {}
    audio_segments = []
    sample_rate = 44100  # défini manuellement pour correspondre à l'audio d'entrée

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

            if name not in voice_map:
                try:
                    speaker_profile = get_or_create_speaker_profile(name, interface)
                    voice_map[name] = speaker_profile
                except Exception as e:
                    print(f"[ERREUR] Impossible de charger/enregistrer le profil de {name} : {e}")
                    continue

            speaker = voice_map[name]

            gen_config = outetts.GenerationConfig(
                text=dialogue,
                speaker=speaker,
                generation_type=outetts.GenerationType.CHUNKED,
                sampler_config=outetts.SamplerConfig(
                    temperature=0.4,
                    repetition_penalty=1.1,
                    top_k=40,
                    top_p=0.9
                ),
                max_length=8192
            )

            try:
                output = interface.generate(config=gen_config)
                audio_data = np.asarray(output.audio, dtype='float32').flatten()
                pause = np.zeros(int(0.5 * sample_rate), dtype='float32')

                audio_segments.append(audio_data)
                audio_segments.append(pause)
            except Exception as e:
                print(f"[ERREUR] Erreur de synthèse pour {name} : {e}")
                continue

    if audio_segments:
        full_audio = np.concatenate(audio_segments)
        sf.write(output_path, full_audio, sample_rate)
        print(f"\n✅ Audio généré avec succès : {output_path}")
    else:
        print("\n⚠️ Aucun segment audio généré. Vérifie le contenu de ton fichier texte et les profils disponibles.")

if __name__ == "__main__":
    main()
