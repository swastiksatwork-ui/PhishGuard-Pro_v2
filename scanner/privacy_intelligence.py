def analyze_privacy_behaviour(

    network_requests,

    network_responses

):

    suspicious_apis = []

    suspicious_domains = []

    tracking_keywords = [

        "fingerprint",

        "telemetry",

        "tracking",

        "analytics",

        "geo",

        "location",

        "clipboard",

        "beacon",

        "session",

        "device"

    ]

    suspicious_domains_keywords = [

        "sentry",

        "telemetry",

        "analytics",

        "tracking"

    ]

    # REQUEST ANALYSIS
    for req in network_requests:

        url = req.get(
            "url",
            ""
        ).lower()

        # TRACKING KEYWORDS
        for keyword in tracking_keywords:

            if keyword in url:

                suspicious_apis.append(keyword)

        # SUSPICIOUS DOMAINS
        for domain_keyword in suspicious_domains_keywords:

            if domain_keyword in url:

                suspicious_domains.append(url)

    # RESPONSE ANALYSIS
    for res in network_responses:

        body = res.get(
            "body",
            ""
        ).lower()

        for keyword in tracking_keywords:

            if keyword in body:

                suspicious_apis.append(keyword)

    return {

        "privacy_keywords_detected":

            list(set(suspicious_apis)),

        "suspicious_domains_detected":

            list(set(suspicious_domains)),

        "privacy_risk_score":

            len(set(suspicious_apis)) * 5

    }