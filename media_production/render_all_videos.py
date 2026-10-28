import os
import subprocess
import soundfile as sf
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
sr = 48000

os.makedirs("media_production/videos", exist_ok=True)

def build_concat_file(slide_schedule, out_concat_path):
    lines = ["ffconcat version 1.0"]
    for img_path, dur in slide_schedule:
        abs_p = os.path.abspath(img_path).replace("\\", "/")
        lines.append(f"file '{abs_p}'")
        lines.append(f"duration {dur:.3f}")
    # Last file must be repeated per ffconcat spec
    if slide_schedule:
        last_abs = os.path.abspath(slide_schedule[-1][0]).replace("\\", "/")
        lines.append(f"file '{last_abs}'")
    with open(out_concat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Generated concat file: {out_concat_path} with {len(slide_schedule)} slides")

def render_phase_video(phase_name, concat_path, audio_path, output_mp4, duration_sec):
    print(f"\n==================================================")
    print(f"RENDERING: {output_mp4} (Duration: {duration_sec:.1f}s)")
    print(f"==================================================")
    cmd = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-r", "24",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        output_mp4
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error rendering {output_mp4}:")
        print(res.stderr)
        return False
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"SUCCESS! Rendered {output_mp4}: {size_mb:.2f} MB")
    return True

# -------------------------------------------------------------
# PHASE 1 VIDEO SCHEDULE
# -------------------------------------------------------------
def get_phase1_schedule():
    intro_img = "media_production/visuals/slides/master_intro_slate.jpg"
    outro_img = "media_production/visuals/slides/master_outro_slate.jpg"
    
    # Base schedule
    sched = [(intro_img, 4.0)]
    
    # 18 clips
    # p1_01_host, p1_02_retailer, ...
    for i in range(1, 19):
        is_host = (i % 2 != 0)
        q_idx = (i + 1) // 2
        clip_p = f"media_production/audio/phase1/p1_{i:02d}_{'host' if is_host else 'retailer'}.wav"
        d, _ = sf.read(clip_p)
        dur = len(d) / sr + 1.0 # 1.0s gap
        
        if q_idx == 1:
            slide = intro_img
        elif q_idx == 9:
            slide = outro_img
        else:
            actual_q = q_idx - 1
            slide = f"media_production/visuals/slides/p1_q{actual_q:02d}_{'host' if is_host else 'retailer'}.jpg"
            
        sched.append((slide, dur))
        
    sched.append((outro_img, 4.0))
    return sched

# -------------------------------------------------------------
# PHASE 2 VIDEO SCHEDULE
# -------------------------------------------------------------
def get_phase2_schedule():
    intro_img = "media_production/visuals/slides/master_intro_slate.jpg"
    outro_img = "media_production/visuals/slides/master_outro_slate.jpg"
    
    sched = [(intro_img, 4.0)]
    
    for i in range(1, 19):
        is_host = (i % 2 != 0)
        q_idx = (i + 1) // 2
        clip_p = f"media_production/audio/phase2/p2_{i:02d}_{'host' if is_host else 'consumer'}.wav"
        d, _ = sf.read(clip_p)
        dur = len(d) / sr + 1.0
        
        if q_idx == 1:
            slide = intro_img
        elif q_idx == 9:
            slide = outro_img
        else:
            actual_q = q_idx - 1
            slide = f"media_production/visuals/slides/p2_q{actual_q:02d}_{'host' if is_host else 'consumer'}.jpg"
            
        sched.append((slide, dur))
        
    sched.append((outro_img, 4.0))
    return sched

# -------------------------------------------------------------
# PHASE 3 VIDEO SCHEDULE
# -------------------------------------------------------------
def get_phase3_schedule():
    intro_img = "media_production/visuals/slides/master_intro_slate.jpg"
    outro_img = "media_production/visuals/slides/master_outro_slate.jpg"
    s1 = "media_production/visuals/slides/p3_slide_01_matrix.jpg"
    s2 = "media_production/visuals/slides/p3_slide_02_redress_gap.jpg"
    s3 = "media_production/visuals/slides/p3_slide_03_trust_index.jpg"
    s4 = "media_production/visuals/slides/p3_slide_04_recommendations.jpg"
    
    slide_map = [
        ("p3_01_lead", intro_img),
        ("p3_02_co", s1),
        ("p3_03_lead", s1),
        ("p3_04_co", s1),
        ("p3_05_lead", s2),
        ("p3_06_co", s3),
        ("p3_07_lead", s4),
        ("p3_08_co", s4),
        ("p3_09_lead", outro_img)
    ]
    
    sched = [(intro_img, 4.0)]
    for tag, slide in slide_map:
        clip_p = f"media_production/audio/phase3/{tag}.wav"
        d, _ = sf.read(clip_p)
        dur = len(d) / sr + 1.2
        sched.append((slide, dur))
        
    sched.append((outro_img, 4.0))
    return sched

if __name__ == "__main__":
    # 1. Phase 1
    s1 = get_phase1_schedule()
    c1 = "media_production/videos/concat_phase1.txt"
    build_concat_file(s1, c1)
    render_phase_video(
        "Phase 1", c1,
        "media_production/audio/masters/MCM315_Phase1_Retailer_Interview_Master.wav",
        "media_production/videos/MCM315_Phase1_Retailer_Interview_1080p.mp4",
        547.8
    )

    # 2. Phase 2
    s2 = get_phase2_schedule()
    c2 = "media_production/videos/concat_phase2.txt"
    build_concat_file(s2, c2)
    render_phase_video(
        "Phase 2", c2,
        "media_production/audio/masters/MCM315_Phase2_Consumer_Interview_Master.wav",
        "media_production/videos/MCM315_Phase2_Consumer_Interview_1080p.mp4",
        468.1
    )

    # 3. Phase 3
    s3 = get_phase3_schedule()
    c3 = "media_production/videos/concat_phase3.txt"
    build_concat_file(s3, c3)
    render_phase_video(
        "Phase 3", c3,
        "media_production/audio/masters/MCM315_Phase3_Academic_Presentation_Master.wav",
        "media_production/videos/MCM315_Phase3_Academic_Presentation_1080p.mp4",
        360.2
    )

    # 4. Master Full Documentary Video
    # Concat s1 + 3s transition + s2 + 3s transition + s3
    print("\nBuilding Full Master Documentary Video Schedule...")
    trans_img = "media_production/visuals/slides/master_intro_slate.jpg"
    full_sched = s1 + [(trans_img, 3.0)] + s2 + [(trans_img, 3.0)] + s3
    c_full = "media_production/videos/concat_full_documentary.txt"
    build_concat_file(full_sched, c_full)
    render_phase_video(
        "Full Documentary", c_full,
        "media_production/audio/masters/MCM315_Full_Documentary_Master.wav",
        "media_production/videos/MCM315_Consumer_Affairs_Full_Documentary_Master_1080p.mp4",
        1382.1
    )

    print("\n==================================================")
    print("ALL BROADCAST VIDEO MASTERS PRODUCED SUCCESSFULLY!")
    print("==================================================")
