import requests

def get_gene_mutations(gene_symbol):
    """
    Fetch mutations for a given gene symbol using MyVariant.info API
    """
    try:
        url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=all&species=human"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", [])
            results = []
            for hit in hits[:5]:  # Limit to 5 results for display
                mutation = {
                    "gene": gene_symbol,
                    "mutation_id": hit.get("_id", "N/A"),
                    "type": hit.get("snpeff", {}).get("ann", [{}])[0].get("effect", "Unknown"),
                    "variant": hit.get("dbsnp", {}).get("rsid", "N/A"),
                    "hgvs": hit.get("hgvs", "N/A")
                }
                results.append(mutation)
            return results
        else:
            return [{"error": f"Failed to fetch data. Status code: {response.status_code}"}]
    except Exception as e:
        return [{"error": str(e)}]
