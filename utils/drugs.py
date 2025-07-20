# utils/drugs.py

import requests

def fetch_drugs_for_mutation(mutation_id):
    """
    Fetch drug information from MyChem.info using mutation rsID (e.g., 'rs121913529').
    """
    url = f"https://mychem.info/v1/query?q=dbsnp.rsid:{mutation_id}&fields=clinvar.drug_response"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("hits", [])
        drugs = set()

        for hit in hits:
            drug_info = hit.get("clinvar", {}).get("drug_response", [])
            for entry in drug_info:
                drug_name = entry.get("drug_name")
                if drug_name:
                    drugs.add(drug_name)

        if drugs:
            return list(drugs)
        else:
            return ["No drug response info found."]
    
    except Exception as e:
        return [f"API error: {str(e)}"]
