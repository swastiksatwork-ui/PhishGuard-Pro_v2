import json
import re
import sys
import subprocess


def clean_json():

    # Read raw Phi-3 output
    with open("reports/raw_command_center.json", "r", encoding="utf-8") as f:
        report = f.read()

    # Load threat score
    with open("reports/threat_score.json", "r", encoding="utf-8") as f:
        threat = json.load(f)

    threat_score = threat["score"]
    indicator = threat["summary_cards"]["indicators"]

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
    with open("reports/cleaned_command_center.json", "w", encoding="utf-8") as f:
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

    # Build final Command Center JSON
    command_json = {

        "threat_score": threat_score,

        "wallets": obj["wallets"],

        "external_domains": obj["external_domains"],

        "indicators": indicator

    }

    # Save final JSON
    with open("reports/command_center.json", "w", encoding="utf-8") as f:
        json.dump(
            command_json,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 60)
    print("Command Center JSON cleaned successfully.")
    print("=" * 60)

    # Launch next stage
    subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_command_center_image"
    ],
    check=True
)


if __name__ == "__main__":
    clean_json()