import requests

def fetch_diseases(gene_symbol):
    """
    Fetch phenotype/disease associations for a gene using Ensembl REST API.
    """
    url = f"https://rest.ensembl.org/phenotype/gene/homo_sapiens/{gene_symbol}?content-type=application/json"
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()

        if not data:
            return [{"disease": "No disease associations found"}]

        diseases = []
        for item in data:
            disease_name = item.get("phenotype_description", "N/A")
            source = item.get("source", "N/A")
            external_id = item.get("external_id", "N/A")

            diseases.append({
                "disease": disease_name,
                "source": source,
                "external_id": external_id
            })

        return diseases

    except Exception as e:
        return [{"disease": f"Error: {str(e)}"}]
