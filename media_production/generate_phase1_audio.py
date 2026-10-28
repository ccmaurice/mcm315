import asyncio
import os
import edge_tts
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

phase1_dialogues = [
    # Intro
    ("p1_01_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Good morning and welcome. I am an undergraduate student in the Department of Mass Communication at Miva Open University, conducting field research for our Consumer Affairs course, MCM315. Today, we are investigating consumer rights, marketing ethics, product quality standards, and post-purchase redress in the consumer electronics sector, with a specific focus on mid-range Android smartphones. I am here at Computer Village, Ikeja, inside Prime Tech Solutions Limited, with Mr. K. Okafor, the Lead Commercial Distributor, who has over eleven years of wholesale and retail experience. Good morning, Mr. Okafor, and thank you for participating in this academic interview."),

    ("p1_02_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "Good morning. You are welcome. I am glad to assist Miva Open University with this important research into our industry."),

    # Question 1
    ("p1_03_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Let us begin with our first question, Mr. Okafor. In the mid-range smartphone market, is there a substandard version of the product, and how do you distinguish between standard and substandard versions of the product?"),

    ("p1_04_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "Yes, absolutely. Substandard and counterfeit versions are widespread in the open market, particularly through parallel gray-market imports and fraudulent cloning factories. As professional distributors, we distinguish standard from substandard through four primary checks. First, packaging integrity and holographic security seals. Standard units feature crisp micro-embossed printing, flawless typography, and tamper-evident holographic distributor seals. Substandard boxes show slight color mismatches, blurry barcodes, or generic shrink-wrap. Second, IMEI registration. Genuine devices carry dual International Mobile Equipment Identity numbers registered on the GSMA global database and authenticated via the Standards Organisation of Nigeria Conformity Assessment Programme, SONCAP portal. Counterfeits use cloned or invalid check-digit IMEIs. Third, chassis build and weight calibration. Standard units use precision aluminum-alloy frames with exact factory weight tolerances, say 189 grams plus or minus two grams. Clones use lightweight injection-molded plastics, loose button tolerances, and give a hollow acoustic feedback. Fourth, firmware architecture. Clones run older Android versions heavily skinned to look like the latest OS, spoofing fake RAM and storage. We detect this immediately when connecting the phone to hardware diagnostic software."),

    # Question 2
    ("p1_05_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "That is very insightful. Moving to our second question: What are the most common complaints or issues consumers face with this product after purchase?"),

    ("p1_06_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "In our records, customer complaints follow distinct patterns within the first thirty to ninety days. Over fifty-five percent of inquiries involve rapid battery drain and thermal overheating under routine 4G data usage. Consumers expect the advertised 48-hour endurance, but find the phone requires recharging twice daily. Second is charging velocity. Customers report that bundled chargers take 80 to 95 minutes instead of the advertised 38 minutes for a full charge, primarily because internal thermal throttling kicks in to prevent the battery from swelling. Third is storage discrepancy and bloatware. Users complain that non-removable promotional apps and background ad services consume up to 28 gigabytes of the advertised 128 gigabytes internal storage. Lastly, users notice touchscreen micro-latency during high humidity, and find that secondary macro and depth cameras offer virtually negligible photographic quality."),

    # Question 3
    ("p1_07_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Thank you. Our third question touches on quality assurance. How do you ensure that the products you sell meet quality standards?"),

    ("p1_08_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "Quality assurance in a reputable business requires strict procurement discipline. First, we source exclusively through Tier-One manufacturer-authorized national distributors. We bypass informal open-market middlemen entirely. Every consignment comes with certified manufacturer warranty agreements, customs duty clearance, and formal tax invoices. Second, we execute inward batch inspections. When shipments arrive at our warehouse, our technical team verifies shipping manifests, checks tamper seals, and performs random unboxing tests on five percent of the units to verify display, network, and battery functionality. Third, serialized inventory tracking. Each unit is logged into our ERP system by its unique IMEI number upon receipt and at point of sale, ensuring complete traceability directly to official manufacturer service centers."),

    # Question 4
    ("p1_09_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Question four addresses marketing ethics: Are the advertisements and marketing claims about this product accurate? Please explain."),

    ("p1_10_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "To be completely honest with you, consumer electronics advertising involves significant promotional exaggeration. Marketing claims are based on idealized laboratory benchmarks. For example, the advertised 48-hour battery life is measured at 20 percent display brightness, in airplane mode, with zero background data and controlled ambient room temperature. But in real Nigerian conditions, with dual active SIM cards, high screen brightness outdoors, and background data synchronization, the battery lasts twelve to fourteen hours at best. Similarly, the 108 megapixel camera claim relies on nine-in-one pixel-binning, meaning the sensor natively captures a twelve megapixel image. Consumers expect billboard clarity, but get compressed photos that struggle in evening lighting. Furthermore, claiming Gorilla Glass drop resistance makes buyers believe the glass is unbreakable, whereas corner drops on asphalt will shatter the display just like any standard glass."),

    # Question 5
    ("p1_11_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "That brings us directly to question five: How do you handle consumer complaints or returns for any product?"),

    ("p1_12_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "Our return policy reflects our commercial agreement with manufacturers. We provide a conditional seven-day exchange window, but this covers strictly out-of-the-box factory defects. The phone must be returned in pristine physical condition with full packaging and proof of purchase. Retailers do not have the unilateral authority to offer cash refunds. The returned unit must be dispatched to the manufacturer's authorized service center for diagnostic auditing, which takes seven to fourteen working days. If the diagnostic center detects any liquid contact indicator activation, cosmetic dent, or software modification like rooting, the warranty is voided and the return is rejected."),

    # Question 6
    ("p1_13_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Question six: Have you received any consumer feedback claiming that a product they purchased did not match the marketing claims, such as issues with fake versus original products?"),

    ("p1_14_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "Yes, very frequently. Many customers visit our service counter with devices bought from unauthorized online sellers offering thirty percent discounts. In most cases, our diagnostic checks reveal these are cosmetically refurbished motherboards housed in counterfeit shells, or clones with dummy cameras. Another major grievance from legitimate buyers is the omission of advertised accessories. Billboards advertise 67-watt flash charging, but upon opening the box, customers discover the manufacturer excluded the fast charger, requiring them to spend an extra fifteen thousand Naira to buy the compatible brick."),

    # Question 7
    ("p1_15_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Our final question: What consumer protection policies do you have in place to ensure customer satisfaction?"),

    ("p1_16_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "We have implemented three core consumer protection measures. First, transparent purchase documentation. Every buyer receives an itemized computerized receipt stating the phone's full dual IMEI numbers, date of sale, and explicit warranty conditions. Second, point-of-sale verification. Our technicians unbox and test the device live in front of the customer, verifying network connectivity, screen touch, and battery charging before the customer leaves the counter. Third, our warranty escalation desk. We act as an ombudsman for our customers, coordinating directly with the manufacturer's central service center and tracking repairs so the buyer does not face administrative frustration alone."),

    # Conclusion
    ("p1_17_host", "en-NG-EzinneNeural", "+0Hz", "+3%",
     "Mr. Okafor, your expert insights provide an invaluable wholesale perspective on the real-world tensions between marketing claims and consumer reality. On behalf of the Mass Communication Department at Miva Open University, thank you very much for your time and transparency."),

    ("p1_18_retailer", "en-NG-AbeoNeural", "-4Hz", "-2%",
     "It was my pleasure. I wish you and Miva Open University the very best in your academic assessment.")
]

async def generate_speech():
    os.makedirs("media_production/audio/phase1", exist_ok=True)
    for tag, voice, pitch, rate, text in phase1_dialogues:
        mp3_path = f"media_production/audio/phase1/{tag}.mp3"
        wav_path = f"media_production/audio/phase1/{tag}.wav"
        print(f"Generating {tag} ({voice})...")
        communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
        await communicate.save(mp3_path)
        
        # Convert to 48kHz stereo WAV for broadcast standard
        cmd = [ffmpeg, "-y", "-i", mp3_path, "-ar", "48000", "-ac", "2", wav_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    asyncio.run(generate_speech())
    print("Phase 1 audio dialogue generation complete!")
