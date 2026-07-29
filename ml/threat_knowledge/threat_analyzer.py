from ml.threat_knowledge.nazario_db import search_phishing_patterns
from ml.threat_knowledge.urlhaus_db import search_ioc


MALWARE_FAMILIES = [
    "mozi",
    "mirai",
    "agenttesla",
    "asyncrat",
    "redline",
    "emotet",
    "qakbot",
    "trickbot"
]


def analyze(runtime_dump, ocr_text):

    findings = []

    runtime_dump = str(
        runtime_dump
    )

    ocr_text = str(
        ocr_text
    )

    print(
        "\nAnalyzing OCR text..."
    )

    findings.extend(
        search_phishing_patterns(
            ocr_text
        )
    )

    print(
        "\nAnalyzing runtime dump..."
    )

    runtime_lower = runtime_dump.lower()

    for family in MALWARE_FAMILIES:

        if family in runtime_lower:

            print(
                f"Detected malware family: {family}"
            )

            ioc_results = search_ioc(
                family
            )

            if len(ioc_results) > 0:

                findings.append({
                    "type": "malware_family",
                    "family": family,
                    "confidence": "high",
                    "match_count": len(ioc_results)
                })

    return findings


if __name__ == "__main__":

    runtime_dump = """
    Architecture Tags: Mozi
    Network IOC:
    http://115.46.81.185:40498/bin.sh
    """

    ocr_text = """
    Verify your account immediately.

    Your password expires soon.

    Click here to validate.
    """

    results = analyze(
        runtime_dump,
        ocr_text
    )

    print(
        "\n===== FINDINGS ====="
    )

    for finding in results:

        print(
            finding
        )