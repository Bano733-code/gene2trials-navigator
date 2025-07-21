import requests

def fetch_diseases(gene_symbol):
    try:
        url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?concepts=gene:{gene_symbol}&format=json"
        response = requests.get(url)
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
            return [{"disease": "No diseases found for this gene"}]
        return diseases

    except Exception as e:
        return [{"disease": f"Error fetching diseases: {e}"}]
