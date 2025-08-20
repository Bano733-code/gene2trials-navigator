
# 📁 utils/summarizer.py
import requests

def fetch_pubmed_abstracts(gene_symbol):
    try:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={gene_symbol}&retmode=json&retmax=5"
        ids = requests.get(url).json()['esearchresult']['idlist']

        efetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        efetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml"
        }
        xml_data = requests.get(efetch_url, params=efetch_params).text

        from xml.etree import ElementTree as ET
        root = ET.fromstring(xml_data)

        abstracts = []
        for article in root.findall(".//PubmedArticle"):
            title = article.findtext(".//ArticleTitle") or ""
            abstract = article.findtext(".//AbstractText") or ""
            abstracts.append({"title": title, "abstract": abstract})

        return abstracts
    except Exception as e:
        return [{"title": "Error", "abstract": str(e)}]
import os
def summarize_text(text):
    try:
        api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {os.environ['HF_API_TOKEN']}"}
        payload = {"inputs": text}

        res = requests.post(api_url, headers=headers, json=payload)
        res.raise_for_status()

        summary = res.json()[0]['summary_text']
        return summary
    except Exception as e:
        return f"Error summarizing text: {e}"
