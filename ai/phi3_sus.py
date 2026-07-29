import json
import ollama
import sys
import subprocess


# =====================================================
# Helper
# =====================================================

def load_text(path):

    try:

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()

    except FileNotFoundError:

        print(f"[WARNING] Missing file: {path}")

        return ""


# =====================================================
# Load Reports
# =====================================================

runtime_dump = load_text(

    "storage/runtime_dump.txt"

)

moondream_dump = load_text(

    "storage/moondream_dump.json"

)


# =====================================================
# JSON Schema
# =====================================================

SUS_SCHEMA = """
{

    "suspicious_features":[

        {

            "text":"",

            "severity":""

        }

    ],

    "technologies":[

        {

            "name":"",

            "category":""

        }

    ],

    "footer":{

        "target":"",

        "risk":"",

        "scan_time":""

    }

}
"""

# =====================================================
# Prompt
# =====================================================

PROMPT = f"""

You are a deterministic Cybersecurity Feature Extraction Engine.

Your ONLY task is extracting

1. Suspicious Features

2. Technologies Used

from the supplied cybersecurity reports.

DO NOT perform another security assessment.

DO NOT calculate an overall threat score.

DO NOT hallucinate.

Only extract evidence explicitly supported by the supplied reports.

========================================================
RUNTIME DUMP
========================================================

{runtime_dump}

========================================================
MOONDREAM DUMP
========================================================

{moondream_dump}


Return ONLY VALID JSON.

Follow EXACTLY this schema.

{SUS_SCHEMA}

==========================================================================================
SUSPICIOUS FEATURES (runtime_verdict), (moondream_dump)
==========================================================================================

Return the most important suspicious observations.

Examples but not limited to

Requests redirected, External Resources, Third-party APIs, Turnstile, Heavy JavaScript, Hidden Inputs
Multiple Redirects, Dynamic Script Loading, Suspicious Forms, Credential Harvesting, Clipboard Access
Wallet Injection, Obfuscated JavaScript, Mixed Content, Cross-Origin Requests, Unknown CDN,Fingerprinting
Suspicious Endpoints, DOM Manipulation, Cookie Abuse

Never invent findings.

Each suspicious feature must contain

"text"

"severity"

Severity must ONLY be one of

critical, high, medium, low

info

Critical = Likely malicious, Credential theft, Wallet theft, Phishing, Exploit indicators

High = Suspicious scripts, Unknown redirects, Unknown third-party domains, Heavy obfuscation

Medium = External APIs, Dynamic resources, Cross-origin requests

Low = Tracking, Analytics, Minor observations

Info =
Interesting but harmless

Return at most 10 suspicious features.

================================================================================
TECHNOLOGIES (moondream_dump), (runtime_dump)
================================================================================

Extract detected technologies if used in website creation.

Examples but not limited to

HTTPS, TLS, HSTS, HTML5, CSS3, JavaScript, Bootstrap, Tailwind, React, PHP, Node.js, WordPress, MySQL
MongoDB

Only include technologies supported by the reports.

Each technology must contain

"name"

"category"

Category must ONLY be one of

security

frontend

framework

backend

infrastructure

cdn

analytics

database

network

Return duplicates only once.

Maximum 20 technologies.

========================================================
FOOTER
========================================================

footer.target

Return analyzed domain.

If unavailable

return ""

footer.risk

Return

CRITICAL

HIGH

MEDIUM

LOW

SAFE

based ONLY on the supplied verdicts.

footer.scan_time

Return current scan timestamp if present.

Otherwise return "".

========================================================

Never output explanations. Never output Markdown. Never output code fences.

Every JSON string MUST start and end with double quotes ("). Never use single quotes (') anywhere in the JSON.

Do NOT output orphan values. Every number, string, array, or object must belong to exactly one JSON key.

Return ONLY the JSON object.

"""

# =====================================================
# Generate JSON
# =====================================================


def run_sus_json():

    print("=" * 70)
    print("Generating Suspicious Features JSON...")
    print("=" * 70)

    response = ollama.chat(

        model="phi3:latest",

        messages=[

            {

                "role": "user",

                "content": PROMPT
            }
    ],
    options={
        "temperature": 0
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

    print("=" * 70)
    print(report)
    print("=" * 70)

    print("=" * 80)
    print("RAW PHI3 OUTPUT")
    print("=" * 80)
    print(report)
    print("=" * 80)

    with open(
    "reports/raw_sus_json.txt",
    "w",
    encoding="utf-8"
    ) as f:

        f.write(report)

    print("=" * 70)
    print("Raw Suspicious JSON Generated")
    print("=" * 70)

    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.sus_json_cleaner"
    ],
    check=True
)


if __name__ == "__main__":

    run_sus_json()

