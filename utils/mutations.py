# 📁 utils/mutations.py
import requests

def fetch_mutations(gene_symbol):
    try:
        url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=clinvar,dbsnp,cadd"
        res = requests.get(url)
        res.raise_for_status()
        hits = res.json().get("hits", [])

        mutations = []
        for hit in hits:
            variant = {
                "variant_id": hit.get("_id", "N/A"),
                "clinvar_sig": hit.get("clinvar", {}).get("clinical_significance", "N/A"),
                "dbsnp": hit.get("dbsnp", {}).get("rsid", "N/A"),
                "cadd_score": hit.get("cadd", {}).get("phred", "N/A")
            }
            mutations.append(variant)

        return mutations
    except Exception as e:
        return f"Error fetching mutations: {e}"
