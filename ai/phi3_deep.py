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

moondream_dump = load_text(
    "storage/moondream_dump.json"
)

runtime_dump = load_text(
    "storage/runtime_dump.txt"
)

ocr_dump = load_text(
    "storage/screenshot_dump.txt"
)

print("=" * 60)
print("Inspecting website visual appearance...")
print("Analyzing browser runtime behaviour...")
print("Checking JavaScript execution flow...")
print("Scanning for embedded cryptocurrency wallets...")
print("Correlating domains, redirects and URLs...")
print("Inspecting Browser APIs and Event Listeners...")
print("Inspecting Cookies, LocalStorage and SessionStorage...")
print("Searching OCR output for hidden phishing indicators...")
print("Analyzing runtime network requests...")
print("Inspecting API endpoints...")
print("Searching for obfuscated JavaScript...")
print("Inspecting suspicious payloads...")
print("Checking browser fingerprinting behaviour...")
print("Checking anti-bot and anti-analysis mechanisms...")
print("Simulating fake wallet interaction...")
print("Evaluating runtime anomalies...")
print("Generating Deep Runtime Intelligence Report...")
print("=" * 60)


PROMPT = f"""

You are a Senior Runtime Security Analyst.

You specialize in:

 Browser Runtime Analysis, JavaScript Analysis, Phishing Detection, Runtime Behaviour Analysis,
 Browser Security, Web Application Security, Digital Forensics.

You have been provided with runtime evidence collected while interacting with a live website.

The evidence comes from browser execution,
runtime monitoring,
OCR,
and browser simulation.

Treat this as supporting evidence.

Your objective is NOT to determine the final verdict.

Instead determine whether runtime behaviour supports or contradicts a phishing or malicious website.

Never hallucinate.

If evidence conflicts,
mention the conflict.

If evidence is insufficient,
state that.

Pay particular attention to these but not limited to these:

• JavaScript behaviour

• Runtime anomalies

• Browser APIs

• Event listeners

• Redirect behaviour

• Form submissions

• Wallet interactions

• Hidden OCR findings

• URLs

• Domains

• Login forms

• Sensitive keywords

• Browser storage

• Cookies

• Local Storage

• Session Storage

• Network requests

• Obfuscated JavaScript

• API endpoints

• Clipboard access

• Browser fingerprinting

• Anti-bot behaviour

• Window manipulation

• External requests

===========================================================
RUNTIME DUMP
===========================================================

{runtime_dump}

===========================================================
 SCREENSHOT OCR
===========================================================

{ocr_dump}

===========================================================
MOONDREAM
===========================================================
{moondream_dump}

Return your report in the following format.

Based on all runtime evidence analysed, I have synthesized the following runtime assessment.

##### Runtime Behaviour(moondream_dump and runtime_dump):

##### Browser Behaviour(runtime_dump):

##### JavaScript Findings(runtime_dump):

##### OCR Findings(ocr_dump):

##### Any Static Crypto Wallet Present(runtime_dump):

##### Any Dynamic Javascript Crypto Wallet Present(runtime_dump):

##### Behaviour on injecting a fake wallet (runtime_dump):

##### Runtime Threat Indicators(ocr_dump and runtime_dump):

##### Runtime Red Flags(moondream_dump and runtime_dump):

##### Runtime Confidence(ocr_dump and runtime_dump):

##### Suspicious Features(moondream_dump and runtime_dump):

##### Recommendations:

Do not return a json.

Produce only a structured text report.

"""

def run_deep():

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

        "reports/runtime_verdict.txt",

        "w",

        encoding="utf-8"

    ) as logfile:

        logfile.write(report)

    return report

subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_master"
    ],
    check=True
)

if __name__ == "__main__":

    run_deep()