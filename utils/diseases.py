# 📁 utils/diseases.py
import requests

API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def get_ensembl_id_from_symbol(gene_symbol):
    """Convert a gene symbol (e.g., BRCA1) to Ensembl gene ID using Open Targets search API."""
    query = {
        "query": """
            query searchTarget($symbol: String!) {
              search(queryString: $symbol, entityNames: ["target"], page: {index: 0, size: 1}) {
                hits {
                  object {
                    ... on Target {
                      id
                      approvedSymbol
                    }
                  }
                }
              }
            }
        """,
        "variables": {"symbol": gene_symbol}
    }

    res = requests.post(API_URL, json=query)
    res.raise_for_status()
    hits = res.json()["data"]["search"]["hits"]

    if not hits:
        raise ValueError(f"No Ensembl ID found for gene symbol: {gene_symbol}")

    return hits[0]["object"]["id"]  # e.g. "ENSG00000012048"


def fetch_diseases(gene_symbol):
    """Fetch associated diseases for a given gene symbol."""
    try:
        # Step 1: Get Ensembl ID
        ensembl_id = get_ensembl_id_from_symbol(gene_symbol)

        # Step 2: Fetch diseases using Ensembl ID
        query = {
            "query": """
                query geneInfo($ensemblId: String!) {
                  target(ensemblId: $ensemblId) {
                    associatedDiseases(page: {index: 0, size: 100}) {
                      rows {
                        disease {
                          name
                          id
                        }
                        score
                      }
                    }
                  }
                }
            """,
            "variables": {"ensemblId": ensembl_id}
        }

        res = requests.post(API_URL, json=query)
        res.raise_for_status()
        rows = res.json()['data']['target']['associatedDiseases']['rows']

        # Step 3: Format results
        diseases = [
            {
                "disease": row['disease']['name'],
                "id": f"[{row['disease']['id']}](https://www.ebi.ac.uk/ols4/ontologies/efo/terms?obo_id={row['disease']['id']})",
                "score": row['score']
            }
            for row in rows
        ]

        return diseases

    except Exception as e:
        return f"Error fetching diseases: {e}"    
                
