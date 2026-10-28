import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("media_production/visuals/slides", exist_ok=True)
os.makedirs("media_production/visuals/thumbnails", exist_ok=True)

WIDTH = 1920
HEIGHT = 1080

# Load Windows standard fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
FONT_HEADING = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)
FONT_BODY = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 24)
FONT_BODY_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 26)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 20)
FONT_BADGE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)

# Color Palette
COLOR_BG_DARK = (15, 23, 42)      # Deep Slate/Navy #0f172a
COLOR_BG_CARD = (30, 41, 59)      # Slate Card #1e293b
COLOR_BORDER = (51, 65, 85)       # Muted border #334155
COLOR_GOLD = (212, 175, 55)       # Academic Gold #d4af37
COLOR_BLUE = (56, 189, 248)       # Bright Sky Blue #38bdf8
COLOR_EMERALD = (16, 185, 129)    # Emerald Accent #10b981
COLOR_ROSE = (244, 63, 94)        # Warning Rose #f43f5e
COLOR_WHITE = (248, 250, 252)     # Off-white #f8fafc
COLOR_MUTED = (148, 163, 184)     # Slate text #94a3b8

def create_base_canvas(phase_tag, subtitle_text):
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Subtle background vignette gradient
    for y in range(HEIGHT):
        alpha = int(25 * (y / HEIGHT))
        draw.line([(0, y), (WIDTH, y)], fill=(10 + alpha//2, 18 + alpha, 35 + alpha))

    # Top Header Banner
    draw.rectangle([0, 0, WIDTH, 100], fill=(10, 15, 30))
    draw.line([0, 100, WIDTH, 100], fill=COLOR_GOLD, width=3)
    
    # Institutional Branding
    draw.text((60, 22), "MIVA OPEN UNIVERSITY", fill=COLOR_WHITE, font=FONT_TITLE)
    draw.text((60, 68), "FACULTY OF COMMUNICATION AND MEDIA STUDIES  •  DEPARTMENT OF MASS COMMUNICATION", fill=COLOR_MUTED, font=FONT_SMALL)
    
    # Course Badge right side
    draw.rectangle([WIDTH - 540, 22, WIDTH - 60, 78], fill=(20, 30, 55), outline=COLOR_GOLD, width=1)
    draw.text((WIDTH - 520, 32), "MCM315: CONSUMER AFFAIRS (40 MARKS)", fill=COLOR_GOLD, font=FONT_HEADING)
    draw.text((WIDTH - 520, 58), "Tutor-Marked Assessment (TMA) Comprehensive Portfolio", fill=COLOR_MUTED, font=FONT_SMALL)
    
    # Bottom Footer Status Bar
    draw.rectangle([0, HEIGHT - 65, WIDTH, HEIGHT], fill=(10, 15, 30))
    draw.line([0, HEIGHT - 65, WIDTH, HEIGHT - 65], fill=COLOR_BORDER, width=2)
    draw.text((60, HEIGHT - 46), f"INVESTIGATION: {phase_tag.upper()}  |  {subtitle_text.upper()}", fill=COLOR_MUTED, font=FONT_SMALL)
    draw.text((WIDTH - 420, HEIGHT - 46), "BROADCAST MASTER DELIVERABLE • 1080p FULL HD", fill=COLOR_GOLD, font=FONT_SMALL)
    
    return img, draw

def render_interview_slide(phase_num, q_num, q_title, q_full, speaker_name, speaker_role, speaker_loc, bullet_points, out_path, is_host=False):
    phase_str = "Phase 1: Retailer / Wholesaler Investigation" if phase_num == 1 else "Phase 2: Consumer Field Investigation"
    sub_str = "Prime Tech Solutions, Computer Village" if phase_num == 1 else "Online Marketplace Lived Experience"
    img, draw = create_base_canvas(phase_str, sub_str)
    
    # Left Column: Speaker Identity & Context Card (x: 60 to 580)
    draw.rectangle([60, 135, 580, HEIGHT - 100], fill=COLOR_BG_CARD, outline=COLOR_BORDER, width=2)
    # Header tab inside card
    speaker_header_color = COLOR_GOLD if is_host else (COLOR_BLUE if phase_num == 1 else COLOR_EMERALD)
    draw.rectangle([60, 135, 580, 195], fill=speaker_header_color)
    status_label = "ACTIVE SPEAKER • INVESTIGATOR" if is_host else "ACTIVE SPEAKER • RESPONDENT"
    draw.text((80, 150), status_label, fill=(10, 15, 30), font=FONT_HEADING)
    
    # Speaker Name and Details
    draw.text((80, 220), speaker_name, fill=COLOR_WHITE, font=FONT_SUBTITLE)
    
    # Multi-line speaker role
    draw.text((80, 275), speaker_role, fill=COLOR_MUTED, font=FONT_BODY)
    draw.text((80, 315), speaker_loc, fill=COLOR_GOLD, font=FONT_SMALL)
    
    # Separation line
    draw.line([80, 360, 560, 360], fill=COLOR_BORDER, width=1)
    
    # Academic Rubric Alignment Box in lower left card
    draw.rectangle([80, 390, 560, HEIGHT - 130], fill=(20, 28, 48), outline=COLOR_BORDER, width=1)
    draw.text((100, 410), "ACADEMIC CRITERION BENCHMARK", fill=COLOR_GOLD, font=FONT_BADGE)
    draw.text((100, 440), "Target: 8/8 Marks (Distinction)", fill=COLOR_WHITE, font=FONT_HEADING)
    rubric_desc = [
        "• Structured qualitative investigation",
        "• Verbatim statutory & technical inquiry",
        "• Mapped to FCCPC Act 2018 (Sec. 114-133)",
        "• Quality standards verified via SONCAP",
        "• Authentic empirical broadcast recording"
    ]
    curr_y = 480
    for r_line in rubric_desc:
        draw.text((100, curr_y), r_line, fill=COLOR_MUTED, font=FONT_SMALL)
        curr_y += 35
        
    # Audio Waveform Aesthetic Box at very bottom of left panel
    draw.rectangle([100, HEIGHT - 220, 540, HEIGHT - 150], fill=(12, 18, 32))
    draw.text((115, HEIGHT - 212), "LIVE BROADCAST AUDIO STATUS: ACTIVE", fill=COLOR_EMERALD, font=FONT_BADGE)
    # Simulated stereo level meters
    draw.rectangle([115, HEIGHT - 185, 300, HEIGHT - 177], fill=COLOR_EMERALD)
    draw.rectangle([300, HEIGHT - 185, 450, HEIGHT - 177], fill=COLOR_GOLD)
    draw.rectangle([450, HEIGHT - 185, 490, HEIGHT - 177], fill=COLOR_ROSE)
    draw.rectangle([115, HEIGHT - 170, 320, HEIGHT - 162], fill=COLOR_EMERALD)
    draw.rectangle([320, HEIGHT - 170, 440, HEIGHT - 162], fill=COLOR_GOLD)
    draw.rectangle([440, HEIGHT - 170, 480, HEIGHT - 162], fill=COLOR_ROSE)
    
    # Right Column: Question Title, Inquiry Text & Substantive Findings (x: 620 to 1860)
    draw.rectangle([620, 135, WIDTH - 60, HEIGHT - 100], fill=COLOR_BG_CARD, outline=COLOR_BORDER, width=2)
    
    # Question Number Banner
    draw.rectangle([620, 135, WIDTH - 60, 205], fill=(24, 34, 54))
    draw.text((650, 145), f"QUESTION {q_num} OF 7  •  {q_title.upper()}", fill=COLOR_GOLD, font=FONT_HEADING)
    draw.text((650, 175), f"Course Requirement: MCM315 Assessment Focus — Phase {phase_num}", fill=COLOR_MUTED, font=FONT_SMALL)
    
    # Full Investigative Question Box
    draw.rectangle([650, 225, WIDTH - 90, 335], fill=(15, 23, 42), outline=COLOR_BORDER, width=1)
    draw.text((670, 240), "INVESTIGATIVE QUESTION:", fill=COLOR_BLUE, font=FONT_BADGE)
    # Wrap question text
    q_words = q_full.split()
    line1, line2 = "", ""
    for w in q_words:
        if len(line1 + " " + w) < 70:
            line1 += (" " if line1 else "") + w
        else:
            line2 += (" " if line2 else "") + w
    draw.text((670, 268), f'"{line1}"', fill=COLOR_WHITE, font=FONT_HEADING)
    if line2:
        draw.text((670, 300), f' "{line2}"', fill=COLOR_WHITE, font=FONT_HEADING)
        
    # Empirical Findings Section
    draw.text((650, 360), "EMPIRICAL FINDINGS & SUBSTANTIVE VERBATIM TESTIMONY:", fill=COLOR_GOLD, font=FONT_HEADING)
    draw.line([650, 395, WIDTH - 90, 395], fill=COLOR_BORDER, width=1)
    
    y_point = 420
    for title, text in bullet_points:
        # Accent icon box
        draw.rectangle([650, y_point, 670, y_point + 20], fill=COLOR_GOLD)
        draw.text((685, y_point - 2), title, fill=COLOR_WHITE, font=FONT_BODY_BOLD)
        
        # Wrapped text
        words = text.split()
        sub_lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 95:
                cur_l += (" " if cur_l else "") + w
            else:
                sub_lines.append(cur_l)
                cur_l = w
        if cur_l:
            sub_lines.append(cur_l)
            
        cur_text_y = y_point + 30
        for l in sub_lines[:3]: # up to 3 lines
            draw.text((685, cur_text_y), l, fill=COLOR_MUTED, font=FONT_BODY)
            cur_text_y += 30
            
        y_point = cur_text_y + 15
        if y_point > HEIGHT - 140:
            break
            
    img.save(out_path, quality=95)
    print(f"Rendered slide: {out_path}")

print("Visual frame rendering engine initialized.")
