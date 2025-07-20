# utils/mutations.py
import requests

def fetch_mutations(gene_symbol):
    try:
        url = f"https://myvariant.info/v1/query?q=gene.symbol:{gene_symbol}&fields=dbsnp.rsid,cadd.phred,clinvar.clinsig&size=10"
        response = requests.get(url)
        data = response.json().get('hits', [])

        mutations = []
        for entry in data:
            rsid = entry.get('dbsnp', {}).get('rsid', 'N/A')
            cadd_score = entry.get('cadd', {}).get('phred', 'N/A')
            clinical_significance = entry.get('clinvar', {}).get('clinsig', 'N/A')

            mutations.append({
                'rsid': rsid,
                'cadd_score': cadd_score,
                'clinical_significance': clinical_significance
            })

        return mutations
    except Exception as e:
        return [{"error": f"Failed to fetch data: {str(e)}"}]
