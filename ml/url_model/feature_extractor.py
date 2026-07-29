def extract_features(url):

    return {
        "url_length": len(url),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "digit_count": sum(
            c.isdigit()
            for c in url
        ),
        "https": int(
            "https" in url.lower()
        ),
        "ip_present": int(
            any(
                c.isdigit()
                for c in url.split("/")[0]
            )
        )
    }