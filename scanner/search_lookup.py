
from ddgs import DDGS

def search_entity(entity):

    results_list = []

    with DDGS() as ddgs:

        results = ddgs.text(entity, max_results=15)

        for index, result in enumerate(results, start=1):

            results_list.append({
                "rank": index,
                "title": result["title"],
                "url": result["href"]
            })

    return results_list