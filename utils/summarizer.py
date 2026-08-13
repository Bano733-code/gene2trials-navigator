import os
import requests
import xml.etree.ElementTree as ET
from groq import Groq

PUBMED_SEARCH = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
)

PUBMED_FETCH = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
)


# ---------------------------------------------------
# Fetch PubMed papers
# ---------------------------------------------------

def fetch_pubmed_abstracts(gene_symbol, max_results=15):

    try:

        search = requests.get(
            PUBMED_SEARCH,
            params={
                "db": "pubmed",
                "term": gene_symbol,
                "retmode": "json",
                "retmax": max_results,
                "sort": "pub_date"
            },
            timeout=30
        )

        ids = search.json()["esearchresult"]["idlist"]

        if len(ids) == 0:
            return []

        xml = requests.get(
            PUBMED_FETCH,
            params={
                "db": "pubmed",
                "id": ",".join(ids),
                "retmode": "xml"
            },
            timeout=60
        )

        root = ET.fromstring(xml.text)

        papers = []

        for article in root.findall(".//PubmedArticle"):

            title = article.findtext(".//ArticleTitle") or ""

            abstract = ""

            nodes = article.findall(".//AbstractText")

            if nodes:

                abstract = " ".join(
                    [
                        n.text.strip()
                        for n in nodes
                        if n.text
                    ]
                )

            if len(abstract) > 20:

                papers.append(
                    {
                        "title": title,
                        "abstract": abstract
                    }
                )

        return papers

    except Exception as e:

        return [{
            "title": "Error",
            "abstract": str(e)
        }]


# ---------------------------------------------------
# Groq Literature Review
# ---------------------------------------------------

def generate_literature_review(gene_symbol):

    papers = fetch_pubmed_abstracts(gene_symbol)

    if len(papers) == 0:
        return "No PubMed papers found."

    literature = ""

    for i, paper in enumerate(papers):

        literature += f"""
Paper {i+1}
Title:
{paper['title']}
Abstract:
{paper['abstract']}
------------------------------------
"""

    # avoid token overflow
    literature = literature[:22000]

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "❌ GROQ_API_KEY not found."

    api_key = api_key.strip()

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert biomedical scientist.
Read all PubMed abstracts about the gene {gene_symbol}.
Write a comprehensive literature review.
The review should contain:
# Overall Research Summary
Write 2-3 detailed paragraphs.
# Current Research Trends
Bullet points.
# Major Discoveries
Bullet points.
# Research Gaps
Bullet points.
# Future Directions
Bullet points.
Do NOT invent facts.
Use only the supplied papers.
PubMed Papers:
{literature}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1800

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error:\n\n{e}"
