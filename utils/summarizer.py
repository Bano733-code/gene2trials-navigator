from transformers import pipeline
import requests
import xml.etree.ElementTree as ET

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def fetch_pubmed_abstracts(gene, max_count=3):
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={gene}&retmax={max_count}&retmode=json"
    ids = requests.get(search_url).json()["esearchresult"]["idlist"]
    abstracts = []
    for id in ids:
        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id}&retmode=xml"
        xml_data = requests.get(fetch_url).text
        root = ET.fromstring(xml_data)
        article = root.find(".//ArticleTitle")
        abstract = root.find(".//AbstractText")
        if article is not None and abstract is not None:
            abstracts.append({"title": article.text, "abstract": abstract.text})
    return abstracts

def summarize_pubmed_abstracts(gene):
    abstracts = fetch_pubmed_abstracts(gene)
    results = []
    for item in abstracts:
        try:
            summary = summarizer(item["abstract"], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
            results.append({ "title": item["title"], "summary": summary })
        except:
            continue
    return results
