import requests

def fetch_mutations(gene_symbol):
    """
    Fetch mutations for a gene from MyVariant.info API using gene symbol.
    """
    url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=dbsnp.rsid,clinvar.clinical_significance,cadd.phred&size=1000"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("hits", [])

        if not hits:
            return [{
                "mutation": "N/A",
                "clinical_significance": "No results found",
                "cadd_score": "N/A"
            }]

        mutations = []
        for hit in hits:
            # Get rsID
            rsid = hit.get("dbsnp", {}).get("rsid", None)
            rsid = f"rs{rsid}" if rsid else "Not available"

            # Get clinical significance
            significance = hit.get("clinvar", {}).get("clinical_significance", None)
            if isinstance(significance, list):
                significance = ", ".join(significance)
            if not significance or significance.lower() in {"n/a", "none", "0"}:
                significance = "Not reported in ClinVar"

            # Get CADD score
            cadd = hit.get("cadd", {}).get("phred", None)
            cadd = round(cadd, 2) if isinstance(cadd, (int, float)) else "Not available"

            # Append record
            mutations.append({
                "mutation": rsid,
                "clinical_significance": significance,
                "cadd_score": cadd
            })

        return mutations

    except Exception as e:
        return [{
            "mutation": "N/A",
            "clinical_significance": f"Error: {str(e)}",
            "cadd_score": "N/A"
        }]
