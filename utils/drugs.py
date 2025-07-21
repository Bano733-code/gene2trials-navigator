import requests

def fetch_drugs_for_gene(gene_symbol):
    try:
        # Step 1: Search for PubMed articles related to the gene
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": gene_symbol,
            "retmode": "json",
            "retmax": 10
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        id_list = response.json()["esearchresult"]["idlist"]

        if not id_list:
            return [{"drug": "No articles found"}]

        # Step 2: Use PubTator to annotate and find Drug mentions
        pubtator_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson"
        headers = {"Content-Type": "application/json"}
        params = {"pmids": ",".join(id_list)}
        pubtator_response = requests.get(pubtator_url, headers=headers, params=params)
        pubtator_response.raise_for_status()
        data = pubtator_response.json()

        # Step 3: Extract drug mentions
        drugs = []
        seen = set()
        for doc in data.get("documents", []):
            for passage in doc.get("passages", []):
                for anno in passage.get("annotations", []):
                    if anno.get("infons", {}).get("type") == "Chemical":
                        drug_name = anno.get("text", "N/A")
                        drug_id = anno.get("infons", {}).get("identifier", "N/A")
                        if drug_name not in seen:
                            seen.add(drug_name)
                            drugs.append({"drug": drug_name, "PubChem CID": drug_id})

        if not drugs:
            return [{"drug": "No drug mentions found in PubTator"}]

        return drugs

    except Exception as e:
        return [{"drug": f"Error fetching drugs: {str(e)}"}]
