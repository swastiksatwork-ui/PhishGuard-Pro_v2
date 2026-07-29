import os
import json
import re
import sys
import subprocess

from pathlib import Path
from PIL import Image
import ollama

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS = BASE_DIR / "reports"
IMAGES = REPORTS / "images"

STORAGE = BASE_DIR / "storage"

OUTPUT_JSON = REPORTS / "command_center.json"

VT_INPUT = IMAGES / "virustotal.png"
IPQS_INPUT = IMAGES / "ipqs.png"

VT_OUTPUT = IMAGES / "virustotal_top.png"
IPQS_OUTPUT = IMAGES / "ipqs_top.png"

def read_text(path):

    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

runtime = read_text(
    STORAGE / "runtime_dump.txt"
)

moondream = read_text(
    STORAGE / "moondream_dump.json"
)

# Load existing threat score
with open(REPORTS / "threat_score.json", "r", encoding="utf-8") as f:
    threat = json.load(f)

threat_score = threat["score"]   # Change "score" if your key is different
indicator  = threat["summary_cards"]["indicators"]

COMMAND_SCHEMA = """
{
    "wallets": "",
    "external_domains": "",
}
"""
PROMPT = f"""
You are generating JSON for the
PhishGuard Command Center.

Return STRICT JSON.

No markdown.

No explanations.

REPORT

=================================================================
MOONDREAM DUMP
==============================================================

{moondream}

==============================================================
RUNTIME DUMP
=============================================================

{runtime}


Use this schema.

{COMMAND_SCHEMA}


The input files(runtime, moondream, runtime_verdict) contain a large amount of unrelated data.

IGNORE everything except information needed to determine:

1. wallets
2. external_domains
3. indicators

Never reproduce the input.

Never summarize the input.

Never copy any fields from the dumps.

Never output title.

Never output links.

Never output scripts.

Never output text_sample.

Never output network_requests.

The ONLY valid output is exactly this schema:

{{
    "wallets": 0,
    "external domains": 0
}}

"""

def run_command_center():

    response = ollama.chat(

        model="phi3:latest",

        options={
            "temperature": 0.1,
            "num_predict": 400
        },

        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ]
    )

    report = response["message"]["content"].strip()

    print("=" * 70)
    print("COMMAND CENTER JSON")
    print("=" * 70)
    print(repr(report))
    print("=" * 70)

    report = report.replace("```json", "").replace("```", "").strip()

    with open(
        REPORTS / "raw_command_center.json",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print("=" * 70)
    print("Raw Command Center JSON Generated")
    print("=" * 70)

    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.command_center_json_cleaner"
    ],
    check=True
)


if __name__ == "__main__":
    run_command_center()