import requests

def fetch_diseases_via_mygene(gene_symbol):
    url = f"https://mygene.info/v3/query?q=symbol:{gene_symbol}&fields=disgenet"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("hits", [])

        diseases = []
        for hit in hits:
            disgenet = hit.get("disgenet", {})
            if isinstance(disgenet, dict):
                disease = disgenet.get("disease_name")
                if disease:
                    diseases.append(disease)

        return diseases if diseases else ["No diseases found."]
    
    except Exception as e:
        return [f"API error: {str(e)}"]
