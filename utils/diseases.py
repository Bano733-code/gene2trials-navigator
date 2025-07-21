import requests
def fetch_diseases(gene_symbol):
    """
    Fetch disease associations for a gene using Open Targets API.
    """
    try:
        # Step 1: Convert gene symbol to Ensembl ID
        lookup_url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene_symbol}?content-type=application/json"
        lookup_response = requests.get(lookup_url, headers={"Content-Type": "application/json"})
        lookup_response.raise_for_status()
        ensembl_id = lookup_response.json().get("id")

        if not ensembl_id:
            return [{"disease": f"Gene ID not found for {gene_symbol}"}]

        # Step 2: Fetch diseases using Open Targets API
        ot_url = f"https://api.platform.opentargets.org/v3/platform/public/association/filter?target={ensembl_id}"
        ot_response = requests.get(ot_url)
        ot_response.raise_for_status()
        data = ot_response.json().get("data", [])

        if not data:
            return [{"disease": "No disease associations found"}]

        diseases = []
        for item in data:
            disease = item.get("disease", {}).get("name", "N/A")
            score = item.get("association_score", {}).get("overall", "N/A")
            datasource = item.get("disease", {}).get("id", "N/A")
            diseases.append({
                "disease": disease,
                "score": round(score, 3) if isinstance(score, float) else "N/A",
                "source": datasource
            })

        return diseases

    except Exception as e:
        return [{"disease": f"Error: {str(e)}"}]
