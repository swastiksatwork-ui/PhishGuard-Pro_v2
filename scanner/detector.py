import re

def analyze_url(url):

    score = 0
    reasons = []

    suspicious_keywords = [
        "login",
        "scam",
        "verify",
        "secure",
        "account",
        "update",
        "bank",
        "wallet",
        "airdrop",
        "claim",
        "crypto"
    ]

    # Long URL
    if len(url) > 80:
        score += 20
        reasons.append("Very long URL detected")

    # @ symbol
    if "@" in url:
        score += 25
        reasons.append("@ symbol detected")

    # Too many hyphens
    if url.count("-") > 3:
        score += 15
        reasons.append("Excessive hyphens detected")

    # Suspicious keywords
    for word in suspicious_keywords:
        if word in url.lower():
            score += 10
            reasons.append(f"Suspicious keyword: {word}")

    # Ethereum wallet regex
    eth_wallet = re.findall(r'0x[a-fA-F0-9]{40}', url)

    if eth_wallet:
        score += 30
        reasons.append("Ethereum wallet detected")

    # Final verdict
    if score >= 60:
        verdict = "CRITICAL"
    elif score >= 35:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return {
        "score": score,
        "verdict": verdict,
        "reasons": reasons,
        "wallets": eth_wallet
    }