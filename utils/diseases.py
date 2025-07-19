# utils/diseases.py

def get_diseases_for_gene(gene_symbol):
    mock_disease_data = {
        "TP53": ["Li-Fraumeni syndrome", "Breast cancer", "Lung cancer"],
        "BRCA1": ["Hereditary breast and ovarian cancer syndrome"],
        "EGFR": ["Non-small cell lung cancer", "Glioblastoma"],
    }

    return mock_disease_data.get(gene_symbol.upper(), ["No known associated diseases found."])
