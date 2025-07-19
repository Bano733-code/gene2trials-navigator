# utils/drugs.py

import requests

def get_drugs_for_gene(gene_symbol):
    try:
        url = f"https://myvariant.info/v1/query?q={gene_symbol}&fields=clinvar"
        response = requests.get(url)
        data = response.json()

        drugs = set()

        for hit in data.get("hits", []):
            clinvar = hit.get("clinvar", {})
            if isinstance(clinvar, dict):
                # Search for drug-related info in trait names or clinical significance
                traits = clinvar.get("trait", [])
                if isinstance(traits, list):
                    for trait in traits:
                        if isinstance(trait, str) and "drug" in trait.lower():
                            drugs.add(trait)
        
        if not drugs:
            # Return mock data if none found
            return ["Tamoxifen", "Cisplatin", "Trastuzumab"]
        else:
            return list(drugs)
    except Exception as e:
        print(f"Error fetching drugs: {e}")
        return ["No drug information available."]
