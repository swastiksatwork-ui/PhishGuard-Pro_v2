import os
import gc
import json
import sys
import subprocess
from PIL import Image
from ai.moondream_core import model

PROMPT = """

Carefully resize the image because its a full page screenshot so zoom it wherever needed.

You are a phishing-cyber website screenshot analyst. Analyze this image.

Return a JSON object.

The JSON should contain:

- Look for "white coloured box" and find and describe fields such as "Agent Readiness", "Ready",
 "Not Ready","Discoverability", "Control Accessibility", "Bot Access Control", "Protocol Discovery",
 "Discoverability" which includes "Goal", "Result", "Evidence" and "Protocol Discovery" which includes
"Goal", "Result", "Evidence". 

Dont hallucinate.

Only include fields that you can actually observe.

You can invent fields.

Do not repeat keys
...
(Return ONLY valid JSON)
"""

def analyze_image():

    image = Image.open(
    "storage/screenshots/cloudflare/cloudflare_agent_readiness.png"
)

    width, height = image.size

    top_half = image.crop(
        (
            0,              # left
            0,              # top
            width,          # right
            height // 2     # bottom
        )
    )

    top_half.save(
        "storage/screenshots/cloudflare/cloudflare_agent_readiness_top.png"
    )

    w, h = image.size

    image = image.resize(
        (w*4, h*2),
        Image.LANCZOS
    )


    answer = model.query(
        image=image,
        question=PROMPT
    )

    return answer


def run_agent_readiness():

    result = analyze_image()

    with open(
        "storage/moondream/cloudflare_agent_readiness.json",
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

    run_agent_readiness()

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

print("=" * 60)
print("Launching Phi-3 Intelligence Pipeline...")
print("=" * 60)
