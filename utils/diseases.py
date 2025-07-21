import requests

def fetch_diseases(gene_symbol):
    try:
        # Step 1: Get PMIDs from PubMed
        esearch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": gene_symbol,
            "retmode": "json",
            "retmax": 10  # You can increase this if needed
        }
        search_response = requests.get(esearch_url, params=params)
        search_response.raise_for_status()
        id_list = search_response.json()['esearchresult']['idlist']

        if not id_list:
            return [{"disease": "No articles found for this gene"}]

        # Step 2: Get annotations from PubTator
        pubtator_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        headers = {"Content-Type": "application/json"}
        params = {"pmids": ",".join(id_list)}
        pubtator_response = requests.get(pubtator_url, params=params, headers=headers)
        pubtator_response.raise_for_status()
        data = pubtator_response.json()

        # Step 3: Extract diseases from PubTator annotations
        diseases = []
        seen = set()
        for doc in data.get("documents", []):
            pmid = doc.get("id", "N/A")
            for passage in doc.get("passages", []):
                for anno in passage.get("annotations", []):
                    if anno.get("infons", {}).get("type") == "Disease":
                        disease_name = anno.get("text", "N/A")
                        disease_id = anno.get("infons", {}).get("identifier", "N/A")
                        key = (disease_name, disease_id)
                        if key not in seen:
                            seen.add(key)
                            diseases.append({
                                "disease": disease_name,
                                "source": disease_id,
                                "pmid": pmid
                            })

        if not diseases:
            return [{"disease": "No disease mentions found in PubTator for this gene"}]

        return diseases

    except Exception as e:
        return [{"disease": f"Error fetching diseases: {str(e)}"}]
