import os
import subprocess
import numpy as np
import soundfile as sf
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
sr = 48000

os.makedirs("media_production/audio/masters", exist_ok=True)
os.makedirs("media_production/audio/stems", exist_ok=True)

def generate_ambient_bed(duration_sec, base_freq=110, volume=0.03):
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    # Warm harmonic pad (root + fifth + octave + gentle chorus)
    pad = (np.sin(2 * np.pi * base_freq * t) * 0.4 +
           np.sin(2 * np.pi * (base_freq * 1.5) * t + 0.5) * 0.25 +
           np.sin(2 * np.pi * (base_freq * 2.0) * t + 1.0) * 0.2 +
           np.sin(2 * np.pi * (base_freq * 2.5) * t + 0.3) * 0.15)
    # Slow LFO breathing
    lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.08 * t)
    # Very light pink-like air noise
    noise = np.random.normal(0, 0.02, len(t))
    noise = np.cumsum(noise) * 0.005
    noise = noise - np.mean(noise)
    max_n = np.max(np.abs(noise)) + 1e-6
    noise = (noise / max_n) * 0.1
    
    stereo_bed = np.column_stack(((pad * lfo + noise) * volume,
                                  (pad * (1.4 - lfo) + np.roll(noise, 2400)) * volume))
    return stereo_bed.astype(np.float32)

def generate_intro_sting():
    dur = 4.0
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    # Broadcast chime chord (D major / F# / A / D high)
    freqs = [293.66, 369.99, 440.00, 587.33, 880.00]
    sting = np.zeros_like(t)
    for i, f in enumerate(freqs):
        env = np.exp(-t * (1.2 + i * 0.3))
        sting += np.sin(2 * np.pi * f * t) * env * (0.2 / len(freqs))
    # Sub-bass hit at start
    sub = np.sin(2 * np.pi * 65 * t[:int(sr * 0.8)]) * np.exp(-t[:int(sr * 0.8)] * 5) * 0.25
    sting[:len(sub)] += sub
    stereo = np.column_stack((sting, np.roll(sting, 120)))
    return stereo.astype(np.float32)

intro_sting = generate_intro_sting()

def mix_phase(dialogue_list, ambient_base_freq, phase_name, silence_gap=1.2):
    print(f"Mixing {phase_name}...")
    # Calculate timeline and load dialogue clips
    clips = []
    total_time = 4.0 # intro buffer
    
    for filename in dialogue_list:
        path = filename
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        d, file_sr = sf.read(path)
        if file_sr != sr:
            raise ValueError(f"SR mismatch in {path}")
        if len(d.shape) == 1:
            d = np.column_stack((d, d))
        clips.append((total_time, d))
        dur = len(d) / sr
        total_time += dur + silence_gap
        
    total_time += 4.0 # outro buffer
    total_samples = int(total_time * sr)
    master = np.zeros((total_samples, 2), dtype=np.float32)
    
    # 1. Place intro chime
    s_idx = int(0.5 * sr)
    e_idx = min(s_idx + len(intro_sting), total_samples)
    master[s_idx:e_idx] += intro_sting[:e_idx - s_idx] * 0.85
    
    # 2. Add ambient bed throughout
    bed = generate_ambient_bed(total_time, base_freq=ambient_base_freq, volume=0.035)
    # Fade bed in and out
    fade_len = int(2.0 * sr)
    bed[:fade_len] *= np.linspace(0, 1, fade_len).reshape(-1, 1)
    bed[-fade_len:] *= np.linspace(1, 0, fade_len).reshape(-1, 1)
    master += bed[:total_samples]
    
    # 3. Place dialogue clips
    timecodes = []
    for start_t, d in clips:
        st_idx = int(start_t * sr)
        end_idx = min(st_idx + len(d), total_samples)
        # dialogue clean gain
        master[st_idx:end_idx] += d[:end_idx - st_idx] * 0.95
        timecodes.append((start_t, (end_idx - st_idx) / sr))
        
    # Peak normalization to -1.0 dB
    peak = np.max(np.abs(master))
    if peak > 0:
        target_peak = 10 ** (-1.0 / 20.0) # 0.891
        master = master * (target_peak / peak)
        
    wav_out = f"media_production/audio/masters/{phase_name}.wav"
    mp3_out = f"media_production/audio/masters/{phase_name}.mp3"
    
    sf.write(wav_out, master, sr)
    # Convert to 320kbps MP3
    cmd = [ffmpeg, "-y", "-i", wav_out, "-b:a", "320k", mp3_out]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    dur_m = total_time / 60.0
    print(f"Generated {wav_out} & {mp3_out}: Duration = {total_time:.1f}s ({dur_m:.2f} mins)")
    return master, timecodes, total_time

if __name__ == "__main__":
    # Phase 1
    p1_files = [f"media_production/audio/phase1/p1_{i:02d}_{'host' if i%2!=0 else 'retailer'}.wav" for i in range(1, 19)]
    m1, tc1, dur1 = mix_phase(p1_files, 110, "MCM315_Phase1_Retailer_Interview_Master", silence_gap=1.0)
    
    # Phase 2
    p2_files = [f"media_production/audio/phase2/p2_{i:02d}_{'host' if i%2!=0 else 'consumer'}.wav" for i in range(1, 19)]
    m2, tc2, dur2 = mix_phase(p2_files, 123.47, "MCM315_Phase2_Consumer_Interview_Master", silence_gap=1.0)
    
    # Phase 3
    p3_tags = ["p3_01_lead", "p3_02_co", "p3_03_lead", "p3_04_co", "p3_05_lead", "p3_06_co", "p3_07_lead", "p3_08_co", "p3_09_lead"]
    p3_files = [f"media_production/audio/phase3/{tag}.wav" for tag in p3_tags]
    m3, tc3, dur3 = mix_phase(p3_files, 130.81, "MCM315_Phase3_Academic_Presentation_Master", silence_gap=1.2)
    
    # Combined Full Documentary Master
    print("Assembling Complete Full Documentary Audio Master...")
    # Combine m1 + 3s transition + m2 + 3s transition + m3
    gap = np.zeros((int(3.0 * sr), 2), dtype=np.float32)
    full_master = np.vstack((m1, gap, m2, gap, m3))
    
    full_wav = "media_production/audio/masters/MCM315_Full_Documentary_Master.wav"
    full_mp3 = "media_production/audio/masters/MCM315_Full_Documentary_Master.mp3"
    sf.write(full_wav, full_master, sr)
    cmd = [ffmpeg, "-y", "-i", full_wav, "-b:a", "320k", full_mp3]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    full_dur = len(full_master) / sr
    print(f"SUCCESS! Complete Full Documentary Audio Master created: {full_dur:.1f}s ({full_dur/60:.2f} mins)")
