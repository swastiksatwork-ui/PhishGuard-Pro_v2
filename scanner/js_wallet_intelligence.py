import requests
import re
from urllib.parse import urljoin


def analyze_js_wallets(

    base_url,

    scripts,

    wallet_requests

):

    result = {}

    downloaded_scripts = []

    web3_hits = []

    wallet_addresses = []

    rpc_methods = []

    # ---------------- WEB3 INDICATORS ----------------

    web3_indicators = [

        "window.ethereum",
        "ethers",
        "web3",
        "walletconnect",
        "eth_requestaccounts",
        "eth_sendtransaction",
        "personal_sign",
        "wagmi",
        "rainbowkit"

    ]

    # ---------------- RPC METHODS ----------------

    rpc_patterns = [

        "eth_requestAccounts",
        "eth_sendTransaction",
        "personal_sign",
        "wallet_switchEthereumChain"

    ]

    # ---------------- WALLET REGEX ----------------

    eth_pattern = r'0x[a-fA-F0-9]{40}'

    headers = {

        "User-Agent": "Mozilla/5.0"

    }

    # ---------------- DOWNLOAD JS ----------------

    for script in scripts:

        try:

            full_url = urljoin(

                base_url,

                script

            )

            response = requests.get(

                full_url,

                headers=headers,

                timeout=10

            )

            js_content = response.text

            downloaded_scripts.append(

                full_url

            )

            lower_js = js_content.lower()

            # ---------------- WEB3 DETECTION ----------------

            for indicator in web3_indicators:

                if indicator.lower() in lower_js:

                    web3_hits.append(

                        indicator

                    )

            # ---------------- RPC DETECTION ----------------

            for rpc in rpc_patterns:

                if rpc.lower() in lower_js:

                    rpc_methods.append(

                        rpc

                    )

            # ---------------- WALLET EXTRACTION ----------------

            wallets = re.findall(

                eth_pattern,

                js_content

            )

            wallet_addresses.extend(

                wallets

            )

        except Exception:

            continue

    # ---------------- FINAL RESULT ----------------

    result["downloaded_scripts"] = downloaded_scripts

    result["web3_indicators_found"] = list(

        set(web3_hits)

    )

    result["rpc_methods_found"] = list(

        set(rpc_methods)

    )

    result["wallet_addresses_found"] = list(

        set(wallet_addresses)

    )

    result["web3_presence_detected"] = int(

        len(web3_hits) > 0

    )

    result["wallet_connection_detected"] = int(

        len(wallet_requests) > 0

    )

    result["wallet_risk_score"] = (

        len(web3_hits) * 10 +

        len(rpc_methods) * 15 +

        len(wallet_addresses) * 5

    )

    return result