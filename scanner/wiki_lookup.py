import requests


def wikipedia_lookup(term):

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term.strip()}"

    headers = {
        "User-Agent": "PhishGuard-Pro/1.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()

        return {
            "found": True,
            "title": data.get("title"),
            "description": data.get("extract")
        }

    return {
        "found": False
    }


def get_official_website(entity):

    headers = {
        "User-Agent": "PhishGuard-Pro/1.0"
    }

    # Search entity
    search_url = (
        f"https://www.wikidata.org/w/api.php"
        f"?action=wbsearchentities"
        f"&search={entity}"
        f"&language=en"
        f"&format=json"
    )

    response = requests.get(search_url, headers=headers)
    data = response.json()

    if not data["search"]:
        return None

    entity_id = data["search"][0]["id"]

    # Fetch entity data
    entity_url = (
        f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
    )

    response = requests.get(entity_url, headers=headers)
    entity_data = response.json()

    claims = entity_data["entities"][entity_id]["claims"]

    # P856 = official website
    if "P856" in claims:

        website = claims["P856"][0]["mainsnak"]["datavalue"]["value"]

        return website

    return None