import asyncio
import os
import edge_tts
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

phase3_dialogues = [
    # Academic Presentation Intro
    ("p3_01_lead", "en-NG-AbeoNeural", "+2Hz", "+3%",
     "Welcome to the Academic Analysis and Synthesis Presentation for Tutor-Marked Assessment MCM315: Consumer Affairs, presented by the Department of Mass Communication at Miva Open University. This investigative presentation synthesizes our supply-side wholesale findings from Phase One and demand-side consumer outcomes from Phase Two, benchmarking our empirical data against the institutional grading rubrics across all five core evaluation criteria to achieve the full forty marks."),

    # Part 1: Comparative Matrix
    ("p3_02_co", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "We begin with Section 5 of our report: the In-Depth Comparative Matrix across the five core product dimensions of the mid-range smartphone. First, Battery Endurance and Power Delivery. The manufacturer heavily advertised up to 48 hours of continuous use and 67-watt flash charging in 38 minutes. Our wholesale respondent revealed that these numbers are synthetic laboratory artifacts tested under zero network traffic and 20 percent brightness. Our consumer's lived reality showed total battery depletion within 8 to 10 hours of routine office tasks, with charging throttled to 85 minutes due to thermal build-up. Under Section 114 and 123 of the FCCPC Act 2018, this constitutes an unlawful deceptive trade description violating the consumer's fundamental Right to Accurate Information."),

    ("p3_03_lead", "en-NG-AbeoNeural", "+2Hz", "+3%",
     "Second, Camera and Optical Clarity. Heavily marketed as a 108 megapixel ultra-clear studio camera, our investigation proved the sensor relies on nine-in-one computational pixel-binning, natively outputting standard 12 megapixel files. The consumer experienced severe shutter lag of up to four seconds per shot and excessive noise in evening lighting. Third, Processing and Storage Architecture. Promoted as 13 gigabytes of RAM and 128 gigabytes of storage, the device actually ships with virtual memory swapped from slower flash storage, while unremovable promotional bloatware consumes 28 gigabytes of user storage, inducing thermal throttling during 20-minute video conferences."),

    ("p3_04_co", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Fourth, Chassis Build and Durability. Advertised with aerospace-grade alloy and Gorilla Glass drop resistance, laboratory teardowns and merchant reports confirm the chassis is electroplated polycarbonate, while glass displays remain highly vulnerable to corner impact fractures. Fifth, Warranty and Return Guarantees. Promoted as a 12-month hassle-free instant replacement guarantee, the operational reality is a 7-day retailer exchange window with strict exclusionary clauses, followed by a 14-day service center diagnostic wall requiring upfront fees with no temporary loaner device."),

    # Part 2: The Redress Gap & Theoretical Framing
    ("p3_05_lead", "en-NG-AbeoNeural", "+2Hz", "+3%",
     "This brings us to a foundational insight of our investigation: The Redress Gap and Theoretical Framing. In consumer affairs jurisprudence, this market exemplifies George Akerlof's 1970 Lemons Principle. Severe information asymmetry exists between manufacturers who possess full technical insight into hardware limitations and consumers who rely on promotional representations. While commercial law permits subjective advertising puffery, Section 123 of the FCCPC Act establishes that objective, quantifiable technical metrics—such as 48 hours battery or 67 watt charging—constitute binding express warranties. The institutional buck-passing between online platforms, merchants, and service centers creates systemic friction-induced abandonment, forcing consumers to bear the financial burden of defective commerce."),

    # Part 3: Trustworthiness Index
    ("p3_06_co", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "To systematically evaluate consumer reliability, our report established the Consumer Trustworthiness Index across four parameters. Hardware Durability scored 7.0 out of 10, reflecting stable core silicon. Marketing Veracity scored 4.0 out of 10 due to distorted specifications. Post-Purchase Redress scored a dismal 3.5 out of 10 due to severe procedural friction. Economic Value scored 6.5 out of 10. The Overall Trust Composite stands at 5.25 out of 10, designating the product category as Moderate Risk, where the consumer receives functional utility but suffers a significant expectation deficit and virtually zero post-purchase redress."),

    # Part 4: Strategic Recommendations
    ("p3_07_lead", "en-NG-AbeoNeural", "+2Hz", "+3%",
     "To satisfy Criterion Five of the institutional rubric, our report articulates an actionable four-tiered reform framework. Tier One, for Manufacturers: Mandatory standardized real-world battery endurance ratings on retail packaging, cryptographic tamper-evident QR codes linked to public anti-counterfeiting verification portals, and a maximum 72-hour warranty turnaround guarantee with temporary loaner phones. Tier Two, for Retailers and E-commerce Platforms: Immediate elimination of unlawful 'goods once sold cannot be returned' signage, transparent 14-day unconditional return windows for non-conforming goods, and escrow-based marketplace payment holding until consumer acceptance."),

    ("p3_08_co", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Tier Three, for Consumers: Pre-purchase due diligence through independent third-party consumer reviews, point-of-sale IMEI authentication against the GSMA and SONCAP portals before leaving sales counters, and prompt dispute escalation to regulatory bodies. Tier Four, for Regulatory Authorities—the FCCPC and Standards Organisation of Nigeria: Randomized market surveillance audits on consumer electronics and accessories, establishment of a digital Small Claims Dispute Portal with automated 14-day statutory mediation deadlines, and deterrent punitive financial penalties on corporate entities that engage in deceptive trade practices."),

    # Conclusion
    ("p3_09_lead", "en-NG-AbeoNeural", "+2Hz", "+3%",
     "In conclusion, this comprehensive investigation demonstrates that protecting consumer rights in the digital age requires closing the gap between statutory guarantees and daily retail enforcement. On behalf of the student research team at Miva Open University, Department of Mass Communication, thank you for your attention.")
]

async def generate_speech():
    os.makedirs("media_production/audio/phase3", exist_ok=True)
    for tag, voice, pitch, rate, text in phase3_dialogues:
        mp3_path = f"media_production/audio/phase3/{tag}.mp3"
        wav_path = f"media_production/audio/phase3/{tag}.wav"
        print(f"Generating {tag} ({voice})...")
        communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
        await communicate.save(mp3_path)
        
        # Convert to 48kHz stereo WAV for broadcast standard
        cmd = [ffmpeg, "-y", "-i", mp3_path, "-ar", "48000", "-ac", "2", wav_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    asyncio.run(generate_speech())
    print("Phase 3 audio dialogue generation complete!")
