from urllib.parse import urlparse

def analyze_network(network_requests):

    anti_bot_services = []

    crypto_requests = []

    telemetry_services = []

    suspicious_post_requests = []

    external_domains = []

    for req in network_requests:

        url = req["url"].lower()

        method = req.get("method","")

        domain = urlparse(url).netloc

        # ---------------- ANTI BOT ----------------

        anti_bot_keywords = [

            "awswaf",

            "captcha",

            "challenge",

            "cloudflare"

        ]

        for word in anti_bot_keywords:

            if word in url:

                anti_bot_services.append(url)

        # ---------------- CRYPTO INFRA ----------------

        crypto_keywords = [

            "wallet",

            "web3",

            "alchemy",

            "infura",

            "metamask",

            "walletconnect",

            "rpc"

        ]

        for word in crypto_keywords:

            if word in url:

                crypto_requests.append(url)

        # ---------------- TELEMETRY ----------------

        telemetry_keywords = [

            "sentry",

            "analytics",

            "telemetry",

            "metrics"

        ]

        for word in telemetry_keywords:

            if word in url:

                telemetry_services.append(url)

        # ---------------- POST REQUESTS ----------------

        if method == "POST":

            suspicious_post_requests.append(url)

        # ---------------- EXTERNAL DOMAINS ----------------

        if "binance.com" not in domain:

            external_domains.append(domain)

    return {

        "anti_bot_services":

        list(set(anti_bot_services)),

        "crypto_requests":

        list(set(crypto_requests)),

        "telemetry_services":

        list(set(telemetry_services)),

        "suspicious_post_requests":

        list(set(suspicious_post_requests)),

        "external_domains":

        list(set(external_domains))

    }