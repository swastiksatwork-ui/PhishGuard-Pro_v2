from urllib.parse import urlparse
import os
import sys
import subprocess
import re
import pandas as pd
import json
import joblib
import shared
from scanner.domain_intelligence import get_domain_intelligence
from scanner.js_wallet_intelligence import analyze_js_wallets
from scanner.playwright_scraper import playwright_scrape
from scanner.playwright_scraper_emulation_test import playwright_scrape_emulation
from scanner.network_intelligence import analyze_network
from scanner.privacy_intelligence import analyze_privacy_behaviour
from malware.malware_search import run_malware_scanners
from scanner.screenshot_ocr import run_ocr
from ml.threat_knowledge.threat_analyzer import analyze
from autogluon.tabular import TabularPredictor
from utils.feature_translator import translate
from autogluon.tabular import TabularPredictor
from scanner.scraper import scrape_website
from scanner.wiki_lookup import wikipedia_lookup
from scanner.wiki_lookup import get_official_website
from scanner.search_lookup import search_entity
from utils.tee import Tee
import time
import threading


original_stdout = sys.stdout

# Clear runtime dump

with open(
    "storage/runtime_dump.txt",
    "w",
    encoding="utf-8"
) as f:
    pass

# Clear screenshot intelligence

with open(
    "storage/screenshot_intelligence.txt",
    "w",
    encoding="utf-8"
) as f:
    pass

# Clear screenshot dump

with open(
    "storage/screenshot_dump.txt",
    "w",
    encoding="utf-8"
) as f:
    pass

# Clear dataset_dump

with open(
    "storage/dataset_dump.txt",
    "w",
    encoding="utf-8"
) as f:
    pass

# Clear fake runtime dump

with open(
    "storage/fake_runtime_dump.txt",
    "w",
    encoding="utf-8"
) as f:
    pass

def extract_features(
    url,
    scraped_data,
    wiki_data,
    official_website,
    search_results
):

    features = {}

    parsed = urlparse(url)

    # ---------------- URL FEATURES ----------------

    features["url_length"] = len(url)

    features["has_https"] = int(parsed.scheme == "https")

    features["hyphen_count"] = url.count("-")

    features["subdomain_count"] = parsed.netloc.count(".")

    suspicious_keywords = [
        "login",
        "verify",
        "secure",
        "wallet",
        "airdrop",
        "claim"
    ]

    keyword_hits = 0

    for word in suspicious_keywords:

        if word in url.lower():
            keyword_hits += 1

    features["suspicious_keyword_count"] = keyword_hits

    # IP detection
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

    features["has_ip_address"] = int(
        bool(re.search(ip_pattern, url))
    )

    # ---------------- SCRAPER FEATURES ----------------

    features["form_count"] = scraped_data.get("form_count", 0)

    features["script_count"] = len(
        scraped_data.get("scripts", [])
    )

    features["image_count"] = len(
        scraped_data.get("images", [])
    )

    # Wallet keyword detection
    text = scraped_data.get("text_sample", "").lower()

    wallet_keywords = [
        "wallet",
        "metamask",
        "seed phrase",
        "private key",
        "connect wallet"
    ]

    wallet_hits = 0

    for word in wallet_keywords:

        if word in text:
            wallet_hits += 1

    features["wallet_keyword_count"] = wallet_hits

    # ---------------- WIKI FEATURES ----------------

    features["known_entity"] = int(
        wiki_data.get("found", False)
    )

    # Official domain match
    official_match = 0

    if official_website:

        official_domain = urlparse(
            official_website
        ).netloc.replace("www.", "")

        submitted_domain = parsed.netloc.replace("www.", "")

        if official_domain == submitted_domain:
            official_match = 1

    features["official_domain_match"] = official_match

    # ---------------- SEARCH FEATURES ----------------

    frequency = 0

    for result in search_results:

        result_url = result.get("url", "")

        if parsed.netloc in result_url:
            frequency += 1

    features["search_domain_frequency"] = frequency

    return features

urls = [
    shared.submitted_url
       
]

original_stdout = sys.stdout

log_file = open(
    "storage/runtime_dump.txt",
    "w",
    encoding="utf-8"
)

sys.stdout = Tee(original_stdout, log_file)

for url in urls:

    print("\n")
    print("="*60)
    print(f"SCRAPPING.... {url}")
    print("="*60)

    try:

        # Scraper
        scraped_data = scrape_website(url)

        print("\nDEBUG SCRAPER OUTPUT")
        print(scraped_data)
        print(type(scraped_data))

        if isinstance(scraped_data, dict):
            print(scraped_data.keys())

        print("\n")
        print("="*60)

        print("\n")
        print("="*60)
        print("Entity")
        print("="*60)

        # Dynamic entity from scraper

        entity = scraped_data.get("entity")

        if not entity:

            print("ENTITY NOT FOUND")
            print(scraped_data)

            continue

        print(entity)

        print("\n")
        print("="*60)

        print("\n")
        print("="*60)
        print("Final Resolved URL.....")
        print("="*60)

        # Final resolved URL

        final_url = scraped_data["final_url"]

        print(final_url)

        print("\n")
        print("="*60)

        print("\n")
        print("="*60)
        print("Scrapping Wikipedia.....")
        print("="*60)

        # Wiki uses entity

        wiki_data = wikipedia_lookup(
            entity
        )

        print(wiki_data)

        print("\n")
        print("="*60)

        print("\n")
        print("="*60)
        print("Official Website")
        print("="*60)

        official_website = get_official_website(
            entity
        )

        print(official_website)

        print("\n")
        print("="*60)

        print("\n")
        print("="*60)
        print("Searching Results.....")
        print("="*60)

        # Search uses actual URL/domain

        search_results = search_entity(
            final_url
        )

        print(search_results)

        print("\n")
        print("="*60)

    except Exception as e:

        print(
            f"FAILED: {url}"
        )

        print(e)

        continue

# Running Malware scanners 

malware_data = {}

print("\n")
print("="*60)
print("Running Malware Scanners...")
print("="*60)

malware_data = run_malware_scanners(
    final_url
)

print(
    malware_data
)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Domain Cross-Checked.....")
print("="*60)

# Domain intelligence
domain_data = get_domain_intelligence(
    final_url
)
print(domain_data)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Scrapping Website Live.....")
print("="*60)

# Playwright Scraper

playwright_data = {}

playwright_data = playwright_scrape(
    final_url
)

scraped_data["title"] = playwright_data["title"]

scraped_data["text_sample"] = playwright_data["text_sample"]

scraped_data["links"] = playwright_data["links"]

scraped_data["scripts"] = playwright_data["scripts"]

scraped_data["images"] = playwright_data["images"]

print(playwright_data)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Analyzing Network.....")
print("="*60)

# Network Analyzer

network_data = analyze_network(

    playwright_data["network_requests"]

)

print(network_data)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Showing Responses.....")
print("="*60)

# Network Responses

print(

    playwright_data["network_responses"]

)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Checking User credential logging behaviour.....")
print("="*60)

# Analyze Privacy Behaviour

privacy_data = analyze_privacy_behaviour(

    playwright_data["network_requests"],

    playwright_data["network_responses"]

)

print(

    privacy_data

)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Checking for website embedded wallets.....")
print("="*60)

# Wallet Requests

print(

    playwright_data["wallet_requests"]

)

print("\n")
print("="*60)

print("\n")
print("="*60)
print("Checking for wallets during load state...")
print("="*60)


# Wallet intelligence

js_wallet_data = analyze_js_wallets(

scraped_data["final_url"],

scraped_data["scripts"],

playwright_data["wallet_requests"]

)
print(js_wallet_data)

print("\n")
print("="*60)


# Extract Features

features = extract_features(
    url,
    scraped_data,
    wiki_data,
    official_website,
    search_results
)

all_features = {

    "basic_features":
        features,

    "scraper_intelligence":
        scraped_data,

    "domain_intelligence":
        domain_data,

    "wiki_intelligence": {

        "wiki_data":
            wiki_data,

        "official_website":
            official_website

    },

    "search_intelligence":
        search_results,

    "runtime_intelligence": {

        "ethereum_runtime":
            playwright_data.get(
                "ethereum_runtime",
                {}
            ),

        "wallet_requests":
            playwright_data.get(
                "wallet_requests",
                []
            ),

        "network_requests":
            playwright_data.get(
                "network_requests",
                []
            ),

        "network_responses":
            playwright_data.get(
                "network_responses",
                []
            )

    },

    "network_intelligence":
        network_data,

    "privacy_intelligence":
        privacy_data,

    "wallet_intelligence":
        js_wallet_data,

    "malware_intelligence":
        malware_data

}

fake_log = open(
    "storage/fake_runtime_dump.txt",
    "w",
    encoding="utf-8"
)

sys.stdout = Tee(original_stdout, fake_log)

log_file.close()



# Playwright Scraper Fake Emulation Test
emulation_data = playwright_scrape_emulation(
    final_url
)

print(emulation_data)

fake_log.close()

sys.stdout = original_stdout

predictor = TabularPredictor.load(
    "ml/models/url_model"
)

url_model_features = {

    "url_length":
        len(final_url),

    "dot_count":
        final_url.count("."),

    "hyphen_count":
        final_url.count("-"),

    "slash_count":
        final_url.count("/"),

    "digit_count":
        len(
            re.findall(
                r"\d",
                final_url
            )
        ),

    "https":
        int(
            final_url.startswith(
                "https"
            )
        ),

    "ip_present":
        int(
            bool(
                re.search(
                    r"(?:\d{1,3}\.){3}\d{1,3}",
                    final_url
                )
            )
        )
}

ocr_dump = ""

ocr_dump = run_ocr()

print("OCR VALUE:", repr(ocr_dump))
print("OCR TYPE:", type(ocr_dump))

with open(
    "storage/screenshot_dump.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        str(ocr_dump)
    )

#OCR Scrapping

runtime_dump = ""

threat_findings = {}



threat_findings = analyze(
    runtime_dump= runtime_dump,
    ocr_text=ocr_dump
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset_dump_path = os.path.join(
    BASE_DIR,
    "..",
    "storage",
    "dataset_dump.txt"
)

log_file = open(
    dataset_dump_path,
    "w",
    encoding="utf-8"
)

sys.stdout = Tee(original_stdout, log_file)

print("\n===== URL MODEL FEATURES =====")
print(url_model_features)

feature_df = pd.DataFrame(
    [url_model_features]
)

print("\n===== Calculating.... FEATURE DF =====")
print(feature_df)

print("\n===== Publishing..... FEATURE DF COLUMNS =====")
print(feature_df.columns.tolist())

url_prediction = predictor.predict(
    feature_df
)

url_probability = predictor.predict_proba(
    feature_df
)

print("\n===== TRANSLATED FEATURES generated.... =====")

translated_features = translate(
    features,
    final_url
)

print(translated_features)

feature_predictor = TabularPredictor.load(
    "ml/models/feature_model"
)

feature_df = pd.DataFrame(
    [translated_features]
)

print("\n===== FEATURE DF created.... =====")
print(feature_df)

print("\n===== FEATURE DF COLUMNS created...... =====")
print(
    feature_df.columns.tolist()
)

feature_prediction = (
    feature_predictor.predict(
        feature_df
    )
)

feature_probability = (
    feature_predictor.predict_proba(
        feature_df
    )
)

print("\n===== FEATURE MODEL RESULT published.... =====")
print(feature_prediction)

print("\n===== Calculating....  FEATURE MODEL PROBABILITY=====")
print(feature_probability)

print(
    "\n===== Calculating...  FEATURE MODEL SCORE ====="
)

print(
    float(
        feature_probability.iloc[0, 1]
    )
)




analysis_report = {

    "resolved_url": final_url,

    "url_prediction":
    int(url_prediction.iloc[0]),

    "url_probability": 
        float(
            url_probability.iloc[0][1]
        ),

    "threat_findings":
        threat_findings

}

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

report_path = os.path.join(
    BASE_DIR,
    "..",
    "storage",
    "analysis_report.json"

)

with open(
    report_path,
    "w",
    encoding = "utf-8"
) as f:
    
    json.dump(
        analysis_report,
        f,
        indent = 4
    )

dataset_path = os.path.join(
    "ml",
    "feature_model",
    "datasets",
    "feature_dataset.csv"
)

dataset_row = {

    "url_length":
        features["url_length"],
    
    "has_https":
        features["has_https"],

    "hyphen_count":
        features["hyphen_count"],

    "subdomain_count":
        features["subdomain_count"],

    "suspicious_keyword_count":
        features["suspicious_keyword_count"],

    "has_ip_address":
        features["has_ip_address"],

    "form_count":
        features["form_count"],

    "script_count":
        features["script_count"],

    "image_count":
        features["image_count"],

    "wallet_keyword_count":
        features["wallet_keyword_count"],

    "known_entity":
        features["known_entity"],

    "official_domain_match":
        features["official_domain_match"],

    "search_domain_frequency":
        features["search_domain_frequency"],

    "label":
        -1

}

df = pd.DataFrame(
    [dataset_row]
)

dataset_path = os.path.join(
    "ml",
    "feature_model",
    "datasets",
    "feature_dataset.csv"
)

os.makedirs(
    os.path.dirname(dataset_path),
    exist_ok=True
)

if os.path.exists(
    dataset_path
):

    df.to_csv(
        dataset_path,
        mode="a",
        header=False,
        index=False
    )

else:

    df.to_csv(
        dataset_path,
        index=False
    )

print(
    f"\n Saved Report: {report_path}"
)

#Isolation Forest

iso_model = joblib.load(
    "ml/models/isolation_forest/isolation_forest.pkl"
)

dataset_row = {

    "url_length":
        features["url_length"],
    
    "has_https":
        features["has_https"],

    "hyphen_count":
        features["hyphen_count"],

    "subdomain_count":
        features["subdomain_count"],

    "suspicious_keyword_count":
        features["suspicious_keyword_count"],

    "has_ip_address":
        features["has_ip_address"],

    "form_count":
        features["form_count"],

    "script_count":
        features["script_count"],

    "image_count":
        features["image_count"],

    "wallet_keyword_count":
        features["wallet_keyword_count"],

    "known_entity":
        features["known_entity"],

    "official_domain_match":
        features["official_domain_match"],

    "search_domain_frequency":
        features["search_domain_frequency"],

    "label":
        -1

}

isolation_row = dataset_row.copy()

isolation_row.pop(
    "label",
    None
)

isolation_row = {

    # ---------------- URL FEATURES ----------------

    "url_length":
        features["url_length"],

    "has_https":
        features["has_https"],

    "hyphen_count":
        features["hyphen_count"],

    "subdomain_count":
        features["subdomain_count"],

    "suspicious_keyword_count":
        features["suspicious_keyword_count"],

    "has_ip_address":
        features["has_ip_address"],

    # ---------------- SCRAPER FEATURES ----------------

    "form_count":
        features["form_count"],

    "script_count":
        features["script_count"],

    "image_count":
        features["image_count"],

    "wallet_keyword_count":
        features["wallet_keyword_count"],

    # ---------------- ENTITY FEATURES ----------------

    "known_entity":
        features["known_entity"],

    "official_domain_match":
        features["official_domain_match"],

    "search_domain_frequency":
        features["search_domain_frequency"],

    # ---------------- URL MODEL ----------------

    "url_probability":
        float(
            url_probability.iloc[0,1]
        ),

    # ---------------- FEATURE MODEL ----------------

    "feature_probability":
        float(
            feature_probability.iloc[0,1]
        ),

    # ---------------- THREAT ANALYZER ----------------

    "threat_count":
        len(
            threat_findings
        ),

    # ---------------- OCR ----------------

    "ocr_text_length":
        len(
            ocr_dump or ""
        ),

    # ---------------- MALWARE ----------------

    "malware_hits":
        len(
            malware_data
        ),

    # ---------------- NETWORK ----------------

    "network_requests":
        len(
            playwright_data.get(
                "network_requests",
                []
            )
        ),

    "network_responses":
        len(
            playwright_data.get(
                "network_responses",
                []
            )
        ),

    # ---------------- WALLET ----------------

    "wallet_requests":
        len(
            playwright_data.get(
                "wallet_requests",
                []
            )
        ),

    # ---------------- PRIVACY ----------------

    "privacy_flags":
        len(
            privacy_data
        ),

    # ---------------- DOMAIN ----------------

    "domain_records":
        len(
            domain_data
        )
}

isolation_dataset_path = os.path.join(
    "ml",
    "datasets",
    "raw",
    "isolation_forest",
    "isolation_dataset.csv"
)

isolation_df = pd.DataFrame(
    [isolation_row]
)

os.makedirs(
    os.path.dirname(
        isolation_dataset_path
    ),
    exist_ok=True
)

if os.path.exists(
    isolation_dataset_path
):

    isolation_df.to_csv(
        isolation_dataset_path,
        mode="a",
        header=False,
        index=False
    )

else:

    isolation_df.to_csv(
        isolation_dataset_path,
        index=False
    )

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        analysis_report,
        f,
        indent=4
    )


iso_model = joblib.load(
    "ml/models/isolation_forest/isolation_forest.pkl"
)

iso_df = pd.DataFrame(
    [isolation_row]
)

iso_prediction = iso_model.predict(
    iso_df
)

iso_score = iso_model.decision_function(
    iso_df
)

print(
    "\n===== ISOLATION FOREST ====="
)

print(
    "Prediction:",
    iso_prediction[0]
)

print(
    "Score:",
    iso_score[0]
)

# ================= OBJECTIVE SCORE =================

# URL Model (0-1)

url_score = float(
    url_probability.iloc[0, 1]
)

# Feature Model (0-1)

feature_score = float(
    feature_probability.iloc[0, 1]
)

# Threat Analyzer (0-1)

threat_score = max(

    0.0,

    1.0 - min(

        len(
            threat_findings
        ) / 10,

        1.0

    )

)

# Isolation Forest (convert anomaly score -> risk)

isolation_score = max(

    0.0,

    min(

        1.0,

        (0.10 - float(iso_score[0])) / 0.20

    )

)

# Convert Risk -> Trust

isolation_score = 1.0 - isolation_score

# Weighted Objective Score (Out of 37)

objective_score = (

    feature_score * 16 +

    url_score * 9 +

    threat_score * 7 +

    isolation_score * 5

)

print(
    "\n===== OBJECTIVE SCORE ====="
)

print(
    f"Feature Model (16%): {feature_score * 16:.2f}"
)

print(
    f"URL Model (9%): {url_score * 9:.2f}"
)

print(
    f"Threat Analyzer (7%): {threat_score * 7:.2f}"
)

print(
    f"Isolation Forest (5%): {isolation_score * 5:.2f}"
)

print(
    f"Total Objective Score: {objective_score:.2f}/37"
)

analysis_report[
    "objective_score"
] = round(
    objective_score,
    2
)

analysis_report[
    "objective_breakdown"
] = {

    "feature_model":
        round(
            feature_score * 16,
            2
        ),

    "url_model":
        round(
            url_score * 9,
            2
        ),

    "threat_analyzer":
        round(
            threat_score * 7,
            2
        ),

    "isolation_forest":
        round(
            isolation_score * 5,
            2
        )

}



print("=" * 60)
print("Initializing Visual Intelligence Engine...")
print("Loading Moondream Vision Model...")
print("Note those process is memory intensive therefore time consuming...")
print("Max time = 15 mins...")
    
print("Grab a Coffee")
print("=" * 60)
    

print("Completely analysed cloudflare_summary")
print("=" * 60)
print("Analysing... cloudflare_security")
    
print("=" * 70)
print("Completely analysed cloudflare_security")
    

print("=" * 60)
print("Analysing... cloudflare_indicators")
    

print("Completely analysed cloudflare_indicators")
print("=" * 60)
print("Analysing.... cloudflare_links")


print("Completely analysed cloudflare_indicators")
print("=" * 60)
print("Analysing.... cloudflare_behaviour")
print("Completely analysed cloudflare_behaviour")

print("=" * 60)
print("Analysing.... cloudflare_network")
print("Completely analysed cloudflare_network")

print("=" * 60)
print("Running Agent Readiness Analysis...")

print("=" * 60)
print("Analyzing Security Vendor Intelligence...")

print("=" * 60)
print("Analyzing VirusTotal Intelligence...")

print("=" * 60)
print("Merging Visual Intelligence Reports...")

print("=" * 60)
print("Loading visual intelligence from Moondream...")
print("Extracting visual security indicators...")
print("Inspecting branding consistency and visual impersonation...")
print("Inspecting login forms and credential harvesting attempts...")
print("Analyzing URL structure and domain composition...")
print("Checking domain reputation and Cloudflare intelligence...")
print("Cross-checking extracted indicators against phishing dataset...")
    
print("Running supervised Machine Learning models...")
   
print("Comparing predictions from ensemble classifiers...")
   
print("Reasoning over Isolation Forest anomaly detection...")

print("Inspecting threat labels and security classifications...")
    
print("Searching for repeated phishing indicators...")

print("Correlating evidence across independent intelligence modules...")

print("Reinforcing confidence from multiple evidence sources...")

print("Generating Primary Cyber Threat Intelligence Report...")

print("=" * 60)

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
    
print("Searching OCR output for hidden phishing indicators...")
    
print("Inspecting API endpoints...")
    
print("Searching for obfuscated JavaScript...")
    
print("Inspecting suspicious payloads...")
    
print("Checking browser fingerprinting behaviour...")

print("Checking anti-bot and anti-analysis mechanisms...")

print("Simulating fake wallet interaction...")
    
print("Evaluating runtime anomalies...")
    
print("Generating Deep Runtime Intelligence Report...")
print("=" * 60)
    

print("=" * 60)
print("Collecting specialist intelligence reports...")

print("Correlating independent analyst findings...")

print("Resolving conflicting observations...")

print("Calculating overall threat confidence...")

print("Estimating confidence through multi-source correlation...")

print("Synthesizing executive threat assessment...")
    
print("Generating Master Cyber Intelligence Report...")
print("=" * 60)


print("[+] Human-readable report saved...")
    

print("=" * 60)
print("Generating Threat Score Dashboard JSON...")
print("=" * 60)


print("Threat Score JSON Created Successfully.")

print("JSON cleaned successfully.")

print("=" * 70)
print("Generating Suspicious Features JSON...")


print("=" * 80)
print("RAW PHI3 OUTPUT")

print("=" * 70)
print("Raw Suspicious JSON Generated")

print("=" * 60)
print("Suspicious Features JSON cleaned successfully.")

print("=" * 70)
print("COMMAND CENTER JSON")
print("=" * 70)

print("=" * 70)
print("Raw Command Center JSON Generated")
print("=" * 70)
    

print("=" * 60)
print("Command Center JSON cleaned successfully.")
print("=" * 60)

print("Saved: IMAGE")

subprocess.run(
    [
        sys.executable,
        "-m",
        "utils.ai_intelligence"
    ],
    check=True
)


log_file.close()
sys.stdout = original_stdout
