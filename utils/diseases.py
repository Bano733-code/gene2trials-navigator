# utils/diseases.py

import requests

def fetch_diseases(gene_symbol):
    """
    Fetch diseases associated with a gene using the DisGeNET API.
    Requires gene symbol (e.g., 'TP53').
    """
    url = f"https://www.disgenet.org/api/gda/gene/{gene_symbol.upper()}"
    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            diseases = {item.get("disease_name") for item in data if "disease_name" in item}
            return list(diseases) if diseases else ["No associated diseases found."]
        elif response.status_code == 404:
            return ["Gene not found in DisGeNET."]
        else:
            return [f"API error: {response.status_code}"]

    except Exception as e:
        return [f"Request failed: {str(e)}"]
