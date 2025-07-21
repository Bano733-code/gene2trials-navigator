# 📁 utils/diseases.py
import requests

def fetch_diseases(gene_symbol):
    try:
        # Using OpenTargets Genetics GraphQL API
        query = {
            "query": """
                query geneInfo($geneSymbol: String!) {
                  target(ensemblIdOrSymbol: $geneSymbol) {
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
            "variables": {"geneSymbol": gene_symbol}
        }
        res = requests.post("https://api.platform.opentargets.org/api/v4/graphql", json=query)
        res.raise_for_status()
        rows = res.json()['data']['target']['associatedDiseases']['rows']

        diseases = [{
            "disease": row['disease']['name'],
            "id": row['disease']['id'],
            "score": row['score']
        } for row in rows]

        return diseases
    except Exception as e:
        return f"Error fetching diseases: {e}"
