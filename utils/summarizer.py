import requests
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def fetch_pubmed_abstracts(gene_symbol, max_results=3):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={gene_symbol}&retmax={max_results}&retmode=json"
    search_res = requests.get(search_url).json()

    ids = search_res.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    id_str = ",".join(ids)
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={id_str}&retmode=json&rettype=abstract"
    abstracts = requests.get(fetch_url).text.split("\n\n")

    return [{"title": f"Paper {i+1}", "abstract": abs_text.strip()} for i, abs_text in enumerate(abstracts)]

def summarize_text(text):
    try:
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        return summary
    except:
        return "Summary could not be generated."
