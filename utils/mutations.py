# utils/mutations.py

import requests

def fetch_mutations(gene_symbol):
    url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=dbsnp.rsid,cadd.phred,clinvar.clinsig"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("hits", [])
        mutations = []
        for hit in hits[:10]:  # Limit to 10 results
            mutations.append({
                "rsid": hit.get("dbsnp", {}).get("rsid", "N/A"),
                "cadd_score": hit.get("cadd", {}).get("phred", "N/A"),
                "clinical_significance": hit.get("clinvar", {}).get("clinsig", "N/A")
            })
        return mutations
    except Exception as e:
        return [{"error": str(e)}]
