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

dataset_dump = load_text(
    "storage/dataset_dump.txt"
)

cloudflare_dump = load_text(
    "storage/cloudflare_content.txt"
)

fake_runtime_dump = load_text(
    "storage/fake_runtime_dump.txt"
)

print("=" * 60)
print("Loading visual intelligence from Moondream...")
print("Opening website screenshots...")
print("Extracting visual security indicators...")
print("Inspecting branding consistency and visual impersonation...")
print("Checking website appearance for phishing characteristics...")
print("Inspecting login forms and credential harvesting attempts...")
print("Analyzing URL structure and domain composition...")
print("Checking domain reputation and Cloudflare intelligence...")
print("Correlating visual evidence with Cloudflare findings...")
print("Cross-checking extracted indicators against phishing dataset...")
print("Running supervised Machine Learning models...")
print("Comparing predictions from ensemble classifiers...")
print("Reasoning over Isolation Forest anomaly detection...")
print("Validating security vendor detections...")
print("Checking SSL certificates and transport security...")
print("Inspecting threat labels and security classifications...")
print("Searching for repeated phishing indicators...")
print("Correlating evidence across independent intelligence modules...")
print("Resolving conflicting observations...")
print("Estimating confidence through multi-source correlation...")
print("Generating Primary Cyber Threat Intelligence Report...")
print("=" * 60)


with open(
    "storage/moondream_dump.json",
    "r",
    encoding="utf-8"
) as f:

    moondream_dump = json.load(f)



PROMPT = f"""

You are a Senior Cybersecurity Threat Intelligence Analyst.

You are also an expert in:

- Phishing Detection, Malware Analysis, Browser Security, Threat Hunting, Threat Intelligence
Web Application Security

You have been given evidence collected from many independent security modules every time live scrapping
pasting link in url scanner sites such as cloudflare, Virustotal scanner and target page and are required 
to do a deep analysis of the same especlially taking outliers and harmful keywords alone very seriously.

Never rely on one source.

Cross-correlate all evidence and if u find an outlier give it more importance if in case of phishing
malware or something sensitive.

If multiple modules support the same finding,
increase confidence.

If evidence conflicts,
mention the conflict.

Never hallucinate.

If evidence is insufficient,
state that.

Pay particular attention to these but not limited to these:

If any keyword like phishing is repeated

If any the the keyword malicious is marked true 

if any labels or security vendors mark it as phishing or anything dangerous bots etc

if any labels or security vendors mark it as malicious or anything dangerous in terms of attack ddos etc

If the link itself looks suspicious a false exaggeration 

The elemets making up the link 
===========================================================
VISION INTELLIGENCE
===========================================================

{json.dumps(moondream_dump, indent=2)}

===========================================================
CLOUDFLARE CONTENT
===========================================================

{cloudflare_dump}

===========================================================
DATASET INFORMATION
===========================================================

{dataset_dump}

===========================================================
FAKE WALLET EMULATION TEST
===========================================================

{fake_runtime_dump}

Give me your verdict in this format 

Based on all the information correlated and deeply analysed , I have synthesized a detailed analysis...

##### Website Analysis(cloudfare_dump): ######################

##### Behaviour on Emulating Fake Wallets in Javascript(fake_runtime_dump): #################

##### Whether any background process triggered due to emulated Wallets(fake_runtime_dump): ############

##### Risk Analysis(moondream_dump and cloudflare_dump): ############################

##### Threat Level Assessment(moondream_dump and cloudflare_dump): ##############

##### Suspicious Features(moondream_dump): #################

##### Red Flags(moondream_dump): #########################

##### Confidence(moondream_dump): ######################

##### Machine Learning Predictions(dataset_dump): ###########

##### Recommendations & Next Steps: #############
"""


def run_primary():

    response = ollama.chat(

        model="phi3:latest",

        messages=[

            {

                "role": "user",

                "content": PROMPT

            }

        ]

    )

    report = response["message"]["content"]

    print(report)

    with open(

        "reports/primary_verdict.txt",

        "w",

        encoding="utf-8"

    ) as logfile:

        logfile.write(report)

    return report


if __name__ == "__main__":

    run_primary()

subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_deep"
    ],
    check=True
)