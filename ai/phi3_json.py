import json
import ollama
import sys
import subprocess

print("=" * 60)
print("AI Intelligence Pipeline Completed Successfully.")
print("Primary Verdict Saved.")
print("Runtime Verdict Saved.")
print("Master Verdict Saved.")
print("Preparing Frontend Intelligence Layer...")
print("=" * 60)

print("=" * 60)
print("Generating Structured Threat Intelligence JSON...")
print("=" * 60)

def load_text(path):

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return f.read()
    
moondream_report = load_text(

    "storage/moondream_report.txt"

)




THREAT_SCHEMA = """


    "objective_score": 0,

    "subjective_score": 0,

    "score": 0,

    "confidence": 0,

    "risk_level": "",

    "needle_angle": 0,

    "summary": {

        "title": "",

        "description": ""

    },

    "summary_cards": {

        "wallets": 0,

        "indicators": 0,

        "threat_score": 0

    },

    "sparkline": [

        0,

        0,

        0,

        0,

        0

    ],

    "gauge": {

        "critical": {

            "min": -10,

            "max": 0

        },

        "severe": {

            "min": 1,

            "max": 20

        },

        "elevated": {

            "min": 21,

            "max": 40

        },

        "guarded": {

            "min": 41,

            "max": 60

        },

        "high": {

            "min": 61,

            "max": 80

        },

        "trusted": {

            "min": 81,

            "max": 100

        }

    }

}
"""

PROMPT = f"""
You are a deterministic cybersecurity JSON generator.

Generate EXACTLY ONE valid JSON object matching this schema:

{THREAT_SCHEMA}

Use ONLY the evidence below.

========= MOONDREAM REPORT =========

{moondream_report}

Rules:

• Use ONLY the evidence in the report.
• Do NOT hallucinate, estimate, invent facts, or use outside knowledge.
• If a value is missing:
  - numbers = 0
  - strings = ""
  - arrays = []

Threat Score Scale:

- CRITICAL : -10 to 0
- SEVERE   : 1 to 20
- ELEVATED : 21 to 40
- GUARDED  : 41 to 60
- HIGH     : 61 to 80
- TRUSTED  : 81 to 99

Using ONLY the evidence and the Threat Score Scale, determine:

- objective_score
- subjective_score (increment or decrement objective_score slightly)
- score ((objective_score + subjective_score) - (objective_score + subjective_score) x 0.25 )

Use the same Threat Score Scale to determine:

- risk_level
- gauge
- gauge.needle_angle
- summary_cards.threat_score
- summary_cards.wallets
- summary_cards.indicators (0 - 100)

Keep the gauge JSON structure EXACTLY as defined in the schema.

Also determine:

- confidence (0-100)
- summary.title (maximum 8 words)
- summary.description (maximum 20 words)

Generate sparkline as EXACTLY five integers (0-100) in this order:

[
    phishing,
    credential_theft,
    wallet_scam,
    malware,
    social_engineering
]

Output Rules:

- Output ONLY the JSON object.
- The first character MUST be '{{'.
- The last character MUST be '}}'.
- Every property name MUST use double quotes.
- Every schema key MUST appear exactly once.
- No duplicate keys.
- No extra keys.
- No markdown.
- No code fences.
- No comments.
- No explanations.
- The output MUST be valid JSON parsable by Python json.loads().
"""


print(len(moondream_report))


def run_threat_json():

    print("=" * 60)
    print("Generating Threat Score Dashboard JSON...")
    print("=" * 60)

    response = ollama.chat(
    model="phi3:latest",
    messages=[
        {
            "role": "user",
            "content": PROMPT
        }
    ],
    options={
        "temperature": 0,
        "num_predict":800
    },
    keep_alive=0
)

    report = response["message"]["content"].strip()

    if report.startswith("```json"):

        report = report[7:]

    elif report.startswith("```"):

        report = report[3:]

    if report.endswith("```"):

        report = report[:-3]

    report = report.strip()

    print("=" * 60)
    print(report)
    print("=" * 60)

    with open("reports/raw_phi3_json.txt", "w", encoding="utf-8") as f:
        f.write(report)

    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.json_cleaner"
    ],
    check=True
)

    print("Threat Score JSON Created Successfully.")


if __name__ == "__main__":

    run_threat_json()
