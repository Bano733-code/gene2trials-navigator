import streamlit as st
from transformers import pipeline

# ---------------------------
# Placeholder mock data
# ---------------------------
gene_to_mutations = {
    "BRCA1": ["185delAG", "5382insC"],
    "TP53": ["R175H", "R248Q"],
    "EGFR": ["L858R", "T790M"],
}

mutation_to_diseases = {
    "185delAG": ["Breast Cancer", "Ovarian Cancer"],
    "5382insC": ["Breast Cancer"],
    "R175H": ["Li-Fraumeni syndrome"],
    "R248Q": ["Multiple cancers"],
    "L858R": ["Lung Cancer"],
    "T790M": ["Lung Cancer (drug resistance)"],
}

disease_to_drugs = {
    "Breast Cancer": ["Tamoxifen", "Olaparib"],
    "Ovarian Cancer": ["Cisplatin"],
    "Li-Fraumeni syndrome": ["Surveillance", "PARP inhibitors"],
    "Multiple cancers": ["Chemotherapy"],
    "Lung Cancer": ["Gefitinib", "Erlotinib"],
    "Lung Cancer (drug resistance)": ["Osimertinib"],
}

disease_to_trials = {
    "Breast Cancer": [
        "This trial investigates the efficacy of Olaparib in BRCA1 mutation carriers.",
        "Study on the preventive impact of Tamoxifen for early-stage breast cancer."
    ],
    "Lung Cancer": [
        "Trial comparing Gefitinib vs Erlotinib in EGFR mutation-positive patients."
    ]
}

# ---------------------------
# Load summarizer pipeline
# ---------------------------
summarizer = pipeline("summarization")

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="Gene2Trials: Mutation to Trials", layout="wide")
st.title("🧬 Gene2Trials: Mutation → Drug Trial Navigator")

# Input box
gene = st.text_input("🔎 Enter a gene symbol (e.g., TP53, BRCA1, EGFR):")

if gene:
    gene = gene.upper()
    st.subheader(f"🔍 Mutations found for {gene}")
    mutations = gene_to_mutations.get(gene, [])
    if mutations:
        st.write(mutations)

        for mutation in mutations:
            diseases = mutation_to_diseases.get(mutation, [])
            for disease in diseases:
                st.markdown(f"### 🦠 Disease: {disease}")

                drugs = disease_to_drugs.get(disease, [])
                if drugs:
                    st.markdown(f"**💊 Drugs:** {', '.join(drugs)}")

                trials = disease_to_trials.get(disease, [])
                if trials:
                    st.markdown("**🧪 Clinical Trial Summaries:**")
                    for i, trial_text in enumerate(trials):
                        summary = summarizer(trial_text, max_length=50, min_length=10, do_sample=False)
                        st.write(f"- {summary[0]['summary_text']}")
    else:
        st.warning("No known mutations found for this gene in our mock dataset.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("This is a mock demo using fake data. Built with ❤️ using Streamlit and HuggingFace transformers.")
