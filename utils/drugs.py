📁 utils/drugs.py
import requests

def fetch_drugs_for_gene(gene_symbol):
    try:
        url = f"https://api.pharmgkb.org/v1/data/gene?name={gene_symbol}"
        headers = {"Accept": "application/json"}
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        gene_data = res.json()
        drugs = []
        for rel in gene_data.get("relatedDrugs", []):
            drugs.append({
                "drug": rel.get("name", "N/A"),
                "pharmgkb_id": rel.get("@id", "N/A")
            })

        return drugs or ["No drug associations found."]
    except Exception as e:
        return f"Error fetching drugs: {e}"
