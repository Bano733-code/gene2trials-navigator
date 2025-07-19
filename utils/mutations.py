# utils/mutations.py

import requests

def fetch_mutations(gene_symbol):
    """
    Fetch mutations for a given gene symbol using MyVariant.info API.
    Returns a list of mutation dictionaries.
    """
    try:
        url = f"https://myvariant.info/v1/query?q=symbol:{gene_symbol}&fields=dbsnp,clinvar,cosmic&size=20"
        response = requests.get(url)
        data = response.json()

        results = []

        hits = data.get("hits", [])
        if not isinstance(hits, list):
            return [{"rsid": "Error", "hgvs": "Unexpected API response", "cosmic_id": ""}]

        for hit in hits:
            dbsnp = hit.get("dbsnp", {})
            clinvar = hit.get("clinvar", {})
            cosmic = hit.get("cosmic", {})

            mutation = {
                "rsid": dbsnp["rsid"] if isinstance(dbsnp, dict) and "rsid" in dbsnp else "N/A",
                "hgvs": clinvar["hgvs"] if isinstance(clinvar, dict) and "hgvs" in clinvar else "N/A",
                "cosmic_id": cosmic["cosmic_id"] if isinstance(cosmic, dict) and "cosmic_id" in cosmic else "N/A",
            }

            results.append(mutation)

        if not results:
            results.append({"rsid": "None", "hgvs": "", "cosmic_id": ""})

        return results

    except Exception as e:
        print(f"Exception occurred: {e}")
        return [{"rsid": "Error", "hgvs": str(e), "cosmic_id": ""}]
