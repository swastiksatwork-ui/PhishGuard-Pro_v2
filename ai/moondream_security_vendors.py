import os
import json
import sys
import subprocess
from PIL import Image 
from ai.moondream_core import model

PROMPT = """

You are a phishing-cyber website screenshot analyst. Analyze this image.

Return many JSON objects.

The JSON should contain:

- Look for "dark-blue coloured square box" and find the "score" given in "community score"  
- print(""int(score)" + security vendors flagged this domain as malicious:" + "int(score)")


Do not reinvent fields.

Do not Hallucinate
Do not repeat keys
...
(Return ONLY valid JSON)
"""

def analyze_image():

    image = Image.open(
    "storage/screenshots/Virustotal/virustotal_detection.png"
)

    answer = model.query(
        image=image,
        question=PROMPT
    )

    return answer


def run_security_vendors():

    result = analyze_image()

    with open(
        "storage/moondream/virustotal_security_vendors.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    return result


if __name__ == "__main__":

    run_security_vendors()

def merge_moondream():

    merged = {}

    folder = "storage/moondream"

    for file in os.listdir(folder):

        if not file.endswith(".json"):
            continue

        path = os.path.join(folder, file)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            merged[
                os.path.splitext(file)[0]
            ] = json.load(f)

    with open(

        "storage/moondream_dump.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            merged,

            f,

            indent=4

        )

    print(
        "Merged successfully."
    )

merge_moondream()

print(".Jsons merged")

