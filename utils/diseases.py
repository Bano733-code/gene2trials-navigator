import requests

def fetch_diseases(gene_symbol):
    """
    Step 1: Convert gene symbol to Ensembl Gene ID
    Step 2: Fetch disease associations using Ensembl Gene ID
    """
    try:
        # Step 1: Convert gene symbol to Ensembl Gene ID
        lookup_url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene_symbol}?content-type=application/json"
        lookup_response = requests.get(lookup_url, headers={"Content-Type": "application/json"})
        lookup_response.raise_for_status()
        gene_data = lookup_response.json()

        ensembl_id = gene_data.get("id")
        if not ensembl_id:
            return [{"disease": f"Gene ID not found for {gene_symbol}"}]

        # Step 2: Use Ensembl Gene ID to get phenotype data
        pheno_url = f"https://rest.ensembl.org/phenotype/gene/homo_sapiens/{ensembl_id}?content-type=application/json"
        pheno_response = requests.get(pheno_url, headers={"Content-Type": "application/json"})
        pheno_response.raise_for_status()
        pheno_data = pheno_response.json()

        if not pheno_data:
            return [{"disease": "No disease associations found"}]

        diseases = []
        for item in pheno_data:
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
