import json
import re
import sys
import subprocess


def clean_json():

    # Read raw Phi-3 output
    with open("reports/raw_threat_chart_json.txt", "r", encoding="utf-8") as f:
        report = f.read()

    # Extract only the JSON object
    start = report.find("{")
    end = report.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found.")

    report = report[start:end + 1]

    # Remove Markdown code fences
    report = report.replace("```json", "")
    report = report.replace("```", "")

    # Remove // comments
    report = re.sub(r"//.*", "", report)

    # Remove trailing commas
    report = re.sub(r",(\s*[}\]])", r"\1", report)

    # Save cleaned JSON for debugging
    with open("reports/cleaned_threat_chart_json.txt", "w", encoding="utf-8") as f:
        f.write(report)

    # Validate JSON
    try:
        obj = json.loads(report)

    except json.JSONDecodeError as e:
        print("=" * 60)
        print("JSON CLEANING FAILED")
        print(e)
        print("=" * 60)
        raise

    # Save valid JSON
    with open("reports/threat_chart.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)

    print("=" * 60)
    print("Threat Chart JSON cleaned successfully.")
    print("=" * 60)

    # Launch next stage
    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_sus"
    ],
    check=True
)


if __name__ == "__main__":
    clean_json()