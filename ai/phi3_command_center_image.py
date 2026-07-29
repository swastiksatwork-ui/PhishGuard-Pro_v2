from PIL import Image
from pathlib import Path
from PIL import Image


# ============================
# VirusTotal Screenshot
# ============================

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS = BASE_DIR / "reports"
STORAGE = BASE_DIR / "storage"

IMAGES = REPORTS / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

VT_INPUT = STORAGE / "screenshots" / "Virustotal" / "virustotal_detection.png"
VT_OUTPUT = IMAGES / "virustotal_top.png"

IPQS_INPUT = STORAGE / "screenshots" / "ipqs" / "ipqs_result.png"
IPQS_OUTPUT = IMAGES / "ipqs_top.png"

def run_command_center_image():

    img = Image.open(VT_INPUT)

    cropped = img.crop((
        0,
        0,
        img.width,
        800
    ))

    cropped = cropped.resize(
        (900, 450),
        Image.LANCZOS
    )

    cropped.save(VT_OUTPUT)

    print("Saved:", VT_OUTPUT)

    img = Image.open(IPQS_INPUT)

    cropped = img.crop((
        0,
        650,
        img.width,
        1600
    ))

    cropped = cropped.resize(
        (900, 450),
        Image.LANCZOS
    )

    cropped.save(IPQS_OUTPUT)

    print("Saved:", IPQS_OUTPUT)

if __name__ == "__main__":

    run_command_center_image()