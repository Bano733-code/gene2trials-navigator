import requests

def get_gene_variants(gene):
    url = f"https://myvariant.info/v1/query?q={gene}&fields=gene.symbol,dbsnp.rsid,cosmic&size=10"
    try:
        response = requests.get(url)
        hits = response.json().get("hits", [])
        return [{ "symbol": h.get("gene", {}).get("symbol"), 
                   "rsid": h.get("dbsnp", {}).get("rsid", ""),
                   "cosmic": h.get("cosmic", {}) } for h in hits]
    except Exception as e:
        return []
