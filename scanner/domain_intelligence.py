import whois
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_domain_intelligence(url):

    parsed = urlparse(url)

    domain = parsed.netloc.replace("www.", "")

    result = {}

    # ---------------- WHOIS ----------------

    try:

        w = whois.whois(domain)

        result["domain"] = domain

        result["registrar"] = w.registrar

        result["creation_date"] = str(w.creation_date)

        result["expiration_date"] = str(w.expiration_date)

        result["country"] = w.country

    except Exception as e:

        result["whois_error"] = str(e)

    # ---------------- DOMAINTOOLS SCRAPE ----------------

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        dt_url = f"https://whois.domaintools.com/{domain}"

        response = requests.get(
            dt_url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        page_text = soup.get_text(
            separator=" ",
            strip=True
        )

        result["domaintools_text"] = page_text[:3000]

    except Exception as e:

        result["domaintools_error"] = str(e)

    return result