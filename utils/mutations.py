# utils/mutations.py

import requests

def fetch_mutations(gene_symbol):
    """
    Fetch mutations for a gene from MyVariant.info API using gene symbol.
    """
    url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=dbsnp.rsid,clinvar.clinical_significance"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("hits", [])

        if not hits:
            return [{"mutation": "N/A", "clinical_significance": "No results found"}]

        mutations = []
        for hit in hits:
            rsid = hit.get("dbsnp", {}).get("rsid", "N/A")
            significance = hit.get("clinvar", {}).get("clinical_significance", "N/A")

            # Sometimes significance can be a list
            if isinstance(significance, list):
                significance = ", ".join(significance)

            mutations.append({
                "mutation": rsid,
                "clinical_significance": significance
            })

        return mutations

    except Exception as e:
        return [{"mutation": "N/A", "clinical_significance": f"Error: {str(e)}"}]
