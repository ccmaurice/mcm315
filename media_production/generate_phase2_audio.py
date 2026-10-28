import asyncio
import os
import edge_tts
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

phase2_dialogues = [
    # Intro
    ("p2_01_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Welcome back to our field investigation for MCM315 Consumer Affairs at Miva Open University. Having examined the supply-side wholesale perspective in Phase One, we now move to Phase Two: the demand-side consumer experience. Joining me today is Ms. A. Ibrahim, a corporate administrative executive who purchased the Android smartphone model under investigation six months ago, using it as her daily communication tool. Good afternoon, Ms. Ibrahim, and thank you for participating in our student research."),

    ("p2_02_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "Good afternoon. Thank you for having me. I am very glad to share my experience because consumer awareness in Nigeria needs much more attention."),

    # Question 1
    ("p2_03_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Let us begin with question one: Have you ever purchased this product online or at a physical shop? If so, did it meet your expectations based on the advertisements or marketing?"),

    ("p2_04_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "I purchased this phone online through a leading e-commerce platform during a major promotional campaign six months ago. The advertisements on social media and billboards made it look like a luxury flagship device, highlighting aerospace-grade durability, super-fast performance, and a stunning design. But when I unboxed it, the reality did not match the hype. The device chassis felt much lighter and made of cheaper plastic than what the ads suggested. It also felt noticeably warm within minutes of initial setup. Worse still, the operating system was cluttered with pre-installed third-party promotional bloatware that I could not uninstall. So right from day one, my expectations were disappointed."),

    # Question 2
    ("p2_05_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Question two: Since you purchased it online, were you satisfied with the overall purchase experience? Please explain the key factors."),

    ("p2_06_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "I was quite dissatisfied, especially with the delivery and fulfillment. First, the platform promised 48-hour express delivery, but the package arrived six business days later. Second, the shipping carton was noticeably dented and lacked tamper-evident security tape. The phone itself was undamaged, but when I inspected the accessory tray, the seller had bundled an ordinary 18-watt basic charger instead of the advertised 67-watt fast charger! Third, the color of the phone in person was a dull reflective blue, completely different from the rich iridescent gradient showcased in official promotional renders."),

    # Question 3
    ("p2_07_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Question three addresses performance claims: Have you experienced the product failing to meet the specific technical claims made in its advertising? Please share your experience."),

    ("p2_08_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "Yes, across three major technical claims. First, battery life. The billboard promised up to 48 hours of continuous use. In reality, just running my routine office apps like WhatsApp, Microsoft Outlook, and LinkedIn drains the battery completely within eight to ten hours, meaning I must charge the phone twice every day. Second, the 108 megapixel camera. The advertising claimed studio-level night photography. But in regular indoor and evening lighting, the photos are full of grain and noise. Furthermore, when taking a 108 megapixel photo, there is an excruciating shutter lag of three to four seconds per shot, making spontaneous pictures impossible. Third, thermal overheating. Whenever I have a twenty-minute video meeting on Teams or Zoom, the upper rear of the phone gets uncomfortably hot, and the screen automatically dims itself to prevent overheating."),

    # Question 4
    ("p2_09_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Question four touches on market hazards: Have you ever received or encountered a substandard or counterfeit product related to this device? How did you identify it?"),

    ("p2_10_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "Yes, and it was a genuinely dangerous incident. About two months after buying the phone, I ordered what was advertised as an original 67-watt manufacturer replacement charger from a marketplace vendor. When it arrived, it felt suspiciously light, almost half the weight of an authentic unit. The prongs were slightly loose, and the brand printing was crooked. Within twenty-five minutes of plugging it into the wall, the charger emitted an acrid burning plastic smell, swelled along its seam, and tripped our home circuit breaker! Upon closer inspection, it lacked the compulsory SONCAP certification stamp and safety fuse. It was a hazardous counterfeit that could have caused a house fire."),

    # Question 5
    ("p2_11_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "That is alarming. Question five: How would you rate the customer service you received when purchasing the product versus when attempting to return or lodge a complaint?"),

    ("p2_12_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "There is an enormous contrast between pre-purchase sales service and post-purchase support. I would rate pre-purchase customer service an eight out of ten. The online checkout was seamless, payment was processed instantly, and automated SMS notifications were prompt. But post-purchase return support was an absolute disaster, barely a two out of ten. When I reached out within seventy-two hours regarding the missing fast charger and the rapid battery drain, the automated chatbot ran in endless loops. When I finally reached human agents, they were dismissive and insisted that electronic devices cannot be returned once the retail box seal is broken."),

    # Question 6
    ("p2_13_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Question six: If you encountered an issue, how did the retailer, marketplace, or manufacturer handle your formal complaint?"),

    ("p2_14_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "It was a masterclass in deflection and passing the buck. The online platform disclaimed all responsibility, claiming they are merely a technology intermediary connecting buyers and sellers. The third-party merchant told me that battery duration is a subjective user feeling rather than a defect, directing me to the manufacturer's authorized service center twenty-five kilometers away. When I traveled to the service center, they demanded an upfront non-refundable diagnostic booking fee of eight thousand Naira and stated the phone would be kept for fourteen working days with no temporary loaner phone provided. Considering transportation costs, the diagnostic fee, and the work disruption of being without a phone for two weeks, I had no choice but to abandon the complaint and absorb the financial loss myself."),

    # Question 7
    ("p2_15_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Our final question, Ms. Ibrahim: Do you feel that consumer protection laws in Nigeria are adequate to ensure consumers receive what they pay for?"),

    ("p2_16_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "On paper, the laws exist. The Federal Competition and Consumer Protection Act of 2018 clearly outlines our rights to fair trade descriptions, refunds, and replacement of substandard goods. But in everyday practice, enforcement is completely out of reach for the common citizen. Filing a formal regulatory petition requires overwhelming paperwork, protracted legalistic procedures, and months of waiting. Vendors operate with impunity because regulatory agencies rarely impose deterrent financial penalties for deceptive advertising or bad-faith warranty evasion. Until regulatory bodies establish swift digital dispute resolution with real financial sanctions, consumers will remain unprotected."),

    # Conclusion
    ("p2_17_host", "en-NG-AbeoNeural", "+4Hz", "+3%",
     "Ms. Ibrahim, your firsthand account perfectly captures the lived consumer experience and highlights the urgent need for institutional reform. Thank you very much for sharing your story with Miva Open University."),

    ("p2_18_consumer", "en-NG-EzinneNeural", "-2Hz", "+1%",
     "Thank you. I truly hope this academic research contributes to better consumer protection standards across Nigeria.")
]

async def generate_speech():
    os.makedirs("media_production/audio/phase2", exist_ok=True)
    for tag, voice, pitch, rate, text in phase2_dialogues:
        mp3_path = f"media_production/audio/phase2/{tag}.mp3"
        wav_path = f"media_production/audio/phase2/{tag}.wav"
        print(f"Generating {tag} ({voice})...")
        communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
        await communicate.save(mp3_path)
        
        # Convert to 48kHz stereo WAV for broadcast standard
        cmd = [ffmpeg, "-y", "-i", mp3_path, "-ar", "48000", "-ac", "2", wav_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    asyncio.run(generate_speech())
    print("Phase 2 audio dialogue generation complete!")
