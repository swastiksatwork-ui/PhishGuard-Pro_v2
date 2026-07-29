
import sys
from pathlib import Path
import subprocess
from ai.moondream_generic import analyze_image, merge_moondream
from ai.moondream_agent_readiness import run_agent_readiness
from ai.moondream_security_vendors import run_security_vendors
from ai.moondream_virustotal import run_virustotal


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

def run_ai_intelligence():

    try:

        print("=" * 60)
        print("Initializing Visual Intelligence Engine...")
        print("Loading Moondream Vision Model...")
        print("Note those process is memory intensive therefore time consuming...")
        print("Max time = 15 mins...")
        print("Grab a Coffee")
        print("=" * 60)

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_summary.png",
            "cloudflare_summary_links.txt",
            "storage/moondream/cloudflare_1_summary.json",
            resize_x=3,
            resize_y=2
        )

        print("Completely analysed cloudflare_summary")

        print("=" * 60)

        print("Analysing... cloudflare_security")

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_security.png",
            "cloudflare_security.txt",
            "storage/moondream/cloudflare_2_security.json",
            resize_x=3,
            resize_y=2
        )

        print("Completely analysed cloudflare_security")

        print("=" * 60)

        print("Analysing... cloudflare_indicators")

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_indicators.png",
            "cloudflare_indicators.txt",
            "storage/moondream/cloudflare_3_indicators.json"
        )

        print("Completely analysed cloudflare_indicators")

        print("=" * 60)

        print("Analysing.... cloudflare_links")

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_links.png",
            "cloudflare_summary_links.txt",
            "storage/moondream/cloudflare_4_links.json"
        )

        print("Completely analysed cloudflare_indicators")

        print("=" * 60)

        print("Analysing.... cloudflare_behaviour")

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_behavior.png",
            "cloudflare_behavior.txt",
            "storage/moondream/cloudflare_5_behavior.json",
            resize_x=3,
            resize_y=2
        )

        print("Completely analysed cloudflare_behaviour")

        print("=" * 60)

        print("Analysing.... cloudflare_network")

        analyze_image(
            "storage/screenshots/cloudflare/cloudflare_network.png",
            "cloudflare_network.txt",
            "storage/moondream/cloudflare_6_network.json",
            resize_x=3,
            resize_y=2
        )

        print("Completely analysed cloudflare_network")

        print("=" * 60)
        print("Running Agent Readiness Analysis...")
        print("=" * 60)

        run_agent_readiness()

        print("=" * 60)
        print("Analyzing Security Vendor Intelligence...")
        print("=" * 60)

        run_security_vendors()

        print("=" * 60)
        print("Analyzing VirusTotal Intelligence...")
        print("=" * 60)

        run_virustotal()

        print("=" * 60)
        print("Merging Visual Intelligence Reports...")
        print("=" * 60)

        merge_moondream()

    except Exception as e:

        print("=" * 60)
        print("AI Intelligence Pipeline Failed")
        print(e)
        print("=" * 60)


    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3"
    ],
    check=True
)  

if __name__ == "__main__":

    run_ai_intelligence()