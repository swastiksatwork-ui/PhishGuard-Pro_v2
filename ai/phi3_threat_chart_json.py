import json
import ollama
import sys
import subprocess


def load_text(path):

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return f.read()


primary_report = load_text(

    "reports/primary_verdict.txt"

)

deep_report = load_text(

    "reports/runtime_verdict.txt"

)

master_report = load_text(

    "reports/master_report.txt"

)


THREAT_CHART_SCHEMA = """
{

    "threat_profile":{

        "phishing":0,

        "wallet_scam":0,

        "credential_theft":0,

        "malware":0,

        "social_engineering":0

    }

}
"""


PROMPT = f"""

You are a Cybersecurity Dashboard JSON Generator.

Your ONLY task is generating the Threat Analytics Radar Chart JSON.

Never perform another cybersecurity analysis.

Never invent findings.

Use ONLY information present in the supplied reports.

==================================================
PRIMARY REPORT
==================================================

{primary_report}

==================================================
DEEP ANALYSIS REPORT
==================================================

{deep_report}

==================================================
MASTER REPORT
==================================================

{master_report}

==================================================

Return ONLY VALID JSON.

The JSON MUST exactly follow this schema.

{THREAT_CHART_SCHEMA}

Rules

1.

Generate ONLY five threat scores.

2.

Each score must be an integer.

3.

Each score must be between 0 and 100.

4.

Use these exact field names.

phishing

wallet_scam

credential_theft

malware

social_engineering

5.

Higher values indicate greater likelihood.

6.

If a category is not mentioned,

return 0.

7.

Never return null.

8.

Never return strings.

9.

Never return decimals.

10.

Return ONLY the JSON object.

"""


def run_phi3_threat_chart_json():

    response = ollama.chat(

        model="phi3:latest",

        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ]

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


    with open("reports/raw_threat_chart_json.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("=" * 60)
    print("Raw Threat Chart JSON Generated")
    print("=" * 60)

    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.threat_chart_json_cleaner"
    ],
    check=True
)

if __name__ == "__main__":

    run_phi3_threat_chart_json()

