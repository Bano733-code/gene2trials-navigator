def fetch_diseases(gene_symbol):
    import requests

    try:
        # Step 1: Convert gene symbol to Ensembl ID
        lookup_url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene_symbol}?content-type=application/json"
        lookup_response = requests.get(lookup_url, headers={"Content-Type": "application/json"})
        lookup_response.raise_for_status()
        ensembl_id = lookup_response.json().get("id")

        if not ensembl_id:
            return [{"disease": f"Gene ID not found for {gene_symbol}"}]

        # Step 2: Fetch diseases using GraphQL
        gql_url = "https://api.platform.opentargets.org/api/v4/graphql"
        query = """
        query($ensemblId: String!) {
          target(ensemblId: $ensemblId) {
            associatedDiseases {
              rows {
                disease {
                  name
                  id
                }
                associationScore {
                  overall
                }
              }
            }
          }
        }
        """
        variables = {"ensemblId": ensembl_id}
        headers = {"Content-Type": "application/json"}
        gql_response = requests.post(gql_url, json={"query": query, "variables": variables}, headers=headers)
        gql_response.raise_for_status()

        rows = gql_response.json()["data"]["target"]["associatedDiseases"]["rows"]

        if not rows:
            return [{"disease": "No disease associations found"}]

        diseases = []
        for item in rows:
            disease_name = item["disease"]["name"]
            disease_id = item["disease"]["id"]
            score = item["associationScore"]["overall"]
            diseases.append({
                "disease": disease_name,
                "score": round(score, 3) if isinstance(score, float) else "N/A",
                "source": disease_id
            })

        return diseases

    except Exception as e:
        return [{"disease": f"Error: {str(e)}"}]
