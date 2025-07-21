import requests

def fetch_diseases(gene_symbol, max_articles=10):
    try:
        # Step 1: Search PubTator for PMIDs related to the gene
        search_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/search?q={gene_symbol}&page=1"
        res = requests.get(search_url)
        res.raise_for_status()
        search_results = res.json()
        pmids = [str(p["pmid"]) for p in search_results.get("results", [])[:max_articles]]

        if not pmids:
            return [{"disease": "No related publications found for gene."}]

        # Step 2: Get annotated concepts for those PMIDs
        annotate_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        response = requests.post(
            annotate_url,
            headers={"Content-Type": "application/json"},
            json={"pmids": pmids}
        )
        response.raise_for_status()
        data = response.json()

        diseases = []
        seen = set()

        for doc in data.get("documents", []):
            for ann in doc.get("annotations", []):
                if ann["infons"].get("type") == "Disease":
                    disease_name = ann["text"]
                    if disease_name not in seen:
                        diseases.append({"disease": disease_name})
                        seen.add(disease_name)

        if not diseases:
            return [{"disease": "No diseases found for this gene in recent literature"}]
        return diseases

    except Exception as e:
        return [{"disease": f"Error fetching diseases: {e}"}]
