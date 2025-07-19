import streamlit as st
import requests
from utils.api_fetch import get_gene_variants
from utils.trial_fetch import get_clinical_trials
from utils.summarizer import summarize_pubmed_abstracts

st.set_page_config(page_title="Gene2Trials", layout="wide")
st.title("🔬 Gene2Trials: Mutation → Drug Trial Navigator")

gene = st.text_input("Enter a gene symbol (e.g., TP53, BRCA1)")

if gene:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧬 Mutations", "🦠 Diseases", "💊 Drugs", "🧪 Clinical Trials", "📚 AI Summary"
    ])

    with tab1:
        st.subheader("Gene Mutations from MyVariant.info")
        variants = get_gene_variants(gene)
        if variants:
            st.write(variants)
        else:
            st.warning("No mutation data found.")

    with tab2:
        st.subheader("Associated Diseases")
        st.write("🧠 Feature coming soon via DisGeNET or OpenTargets!")

    with tab3:
        st.subheader("Drugs")
        st.write("💊 You can integrate DrugBank/PharmGKB in future updates.")

    with tab4:
        st.subheader("Clinical Trials from ClinicalTrials.gov")
        trials = get_clinical_trials(gene)
        if trials:
            st.write(trials)
        else:
            st.warning("No trials found for this gene.")

    with tab5:
        st.subheader("AI-generated Research Summaries from PubMed")
        summaries = summarize_pubmed_abstracts(gene)
        for idx, item in enumerate(summaries):
            st.markdown(f"**{idx+1}. {item['title']}**")
            st.markdown(item['summary'])
            st.markdown("---")
