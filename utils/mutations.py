# utils/mutations.py

import requests

def fetch_mutations(gene_symbol):
    """
    Fetch mutations for a given gene symbol using MyVariant.info API.
    Returns a list of mutation dictionaries.
    """
    try:
        url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=dbsnp.rsid,clinvar.hgvs,cosmic.cosmic_id&size=20"
        response = requests.get(url)
        data = response.json()

        results = []
        for hit in data.get("hits", []):
            mutation = {
                "rsid": hit.get("dbsnp", {}).get("rsid", "N/A") if isinstance(hit.get("dbsnp"), dict) else "N/A",
                "hgvs": hit.get("clinvar", {}).get("hgvs", "N/A") if isinstance(hit.get("clinvar"), dict) else "N/A",
                "cosmic_id": hit.get("cosmic", {}).get("cosmic_id", "N/A") if isinstance(hit.get("cosmic"), dict) else "N/A",
            }
            results.append(mutation)

        return results if results else [{"rsid": "None found", "hgvs": "", "cosmic_id": ""}]

    except Exception as e:
        print(f"Error fetching mutations: {e}")
        return [{"rsid": "Error", "hgvs": str(e), "cosmic_id": ""}]
