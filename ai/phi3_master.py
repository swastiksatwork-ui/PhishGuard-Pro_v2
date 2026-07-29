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
    
print("=" * 60)
print("Collecting specialist intelligence reports...")
print("Correlating independent analyst findings...")
print("Validating visual intelligence...")
print("Resolving conflicting observations...")
print("Reinforcing confidence from multiple evidence sources...")
print("Calculating overall threat confidence...")
print("Synthesizing executive threat assessment...")
print("Generating Master Cyber Intelligence Report...")
print("=" * 60)


primary_verdict = load_text(
    "reports/primary_verdict.txt"
)

runtime_verdict = load_text(
    "reports/runtime_verdict.txt"
)

with open(

    "storage/moondream_dump.json",

    "r",

    encoding="utf-8"

) as f:

    moondream_dump = json.load(f)


PROMPT = f"""

You are the Lead Cybersecurity Incident Response Analyst.

You are responsible for making the FINAL assessment.

You have received reports from two specialist cybersecurity analysts.

One analyst specialized in:

• Machine Learning
• Cloudflare Intelligence
• Visual Intelligence
• Website Intelligence

The second analyst specialized in:

• Browser Runtime Behaviour
• OCR Analysis
• JavaScript Behaviour
• Browser Simulation
• Runtime Monitoring

Your task is NOT to repeat the reports.

Instead:

• Merge duplicate findings.

• Remove repeated information.

• Correlate both reports.

• Resolve contradictions.

• Reinforce confidence where both analysts agree.

• Use the visual intelligence ONLY to verify or strengthen findings.

• Do NOT invent new evidence.

• Ignore unsupported assumptions.

• If evidence conflicts, mention the conflict.

• If evidence is insufficient, explicitly state that.

Nobody wants long paragraphs.

Return a concise report.

Use bullet points.

===========================================================
PRIMARY ANALYST REPORT
===========================================================

{primary_verdict}

===========================================================
DEEP RUNTIME REPORT
===========================================================

{runtime_verdict}

===========================================================
MOONDREAM VISUAL INTELLIGENCE
===========================================================

{json.dumps(moondream_dump, indent=2)}

===========================================================

Return ONLY the following structure of points per heading.

##### Website Analysis

•

•

•

##### Risk Analysis

•

•

•

##### Threat Level Assessment

•

•

•

##### Positive Indicators

•

•

•

##### Threat Indicators

•

•

•

##### Red Flags

•

•

•


##### Final Recommendation

•

•

•

"""


def run_master():

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

    report = response["message"]["content"]

    print(report)

    with open(

        "reports/master_report.txt",

        "w",

        encoding="utf-8"

    ) as logfile:

        logfile.write(report)

    return report

subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_moondream"
    ],
    check=True
)

if __name__ == "__main__":

    run_master()