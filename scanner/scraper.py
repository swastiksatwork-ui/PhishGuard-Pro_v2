import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def scrape_website(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(url, headers=headers, timeout=10)

        final_url = response.url

        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Page Title
        title = soup.title.string.strip() if soup.title else "No Title"

        # Visible Text
        text = soup.get_text(separator=" ", strip=True)

        # Links
        links = []

        for link in soup.find_all("a"):

            href = link.get("href")

            if href:
                links.append(href)

        # Images
        images = []

        for img in soup.find_all("img"):

            src = img.get("src")

            if src:
                images.append(src)

        # Scripts
        scripts = []

        for script in soup.find_all("script"):

            src = script.get("src")

            if src:
                scripts.append(src)

        # Forms
        forms = soup.find_all("form")

        parsed = urlparse(final_url)
        domain = parsed.netloc.replace("www.","")
        entity = domain.split(".",)[0]

        return {

            "final_url": final_url,

            "entity": entity,

            "title": title,

            "text_sample": text[:1000],

            "links": links[:10],

            "images": images[:10],

            "scripts": scripts[:10],

            "form_count": len(forms)
        }

    except Exception as e:

        return {
            "error": str(e)
        }

urls = [
        "http://steam-totp.pages.dev"
]


for url in urls:
    result = scrape_website(
        url
    )

print(result)