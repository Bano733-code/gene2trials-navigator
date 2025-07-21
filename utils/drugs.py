import requests

def fetch_drugs_for_gene(gene_symbol):
    try:
        url = f"https://dgidb.org/api/v2/interactions.json?genes={gene_symbol}"
        res = requests.get(url)
        res.raise_for_status()

        data = res.json()
        interactions = data.get("matchedTerms", [])[0].get("interactions", [])

        if not interactions:
            return [{"drug": "No drug interactions found.", "source": "DGIdb"}]

        drugs = []
        for item in interactions:
            drugs.append({
                "drug": item.get("drugName", "N/A"),
                "interaction_type": item.get("interactionTypes", ["N/A"])[0],
                "source": item.get("sources", ["N/A"])[0]
            })

        return drugs

    except Exception as e:
        return [{"drug": f"Error fetching drugs: {e}"}]
