import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "datasets",
    "raw",
    "threat",
    "Nazario.csv"
)

df = pd.read_csv(
    dataset_path
)

print(
    f"Loaded {len(df)} Nazario records"
)

PHISHING_PATTERNS = [
    "verify your account",
    "verify account",
    "account suspended",
    "password expires",
    "confirm your identity",
    "click here to validate",
    "update your account",
    "login immediately",
    "security alert",
    "unusual activity detected",
    "your account has been limited"
]


def search_phishing_patterns(text):

    text = text.lower()

    findings = []

    for pattern in PHISHING_PATTERNS:

        if pattern in text:

            matches = []

            for _, row in df.iterrows():

                body = str(
                    row["body"]
                ).lower()

                if pattern in body:

                    matches.append({
                        "subject": row["subject"],
                        "sender": row["sender"],
                        "body_preview": str(
                            row["body"]
                        )[:200]
                    })

            findings.append({
                "type": "phishing_phrase",
                "pattern": pattern,
                "confidence": "low",
                "matches": len(matches),
                "examples": matches[:3]
            })

    return findings


if __name__ == "__main__":

    test_text = """
    Verify your account immediately.
    Your password expires soon.
    """

    results = search_phishing_patterns(
        test_text
    )

    print(results)