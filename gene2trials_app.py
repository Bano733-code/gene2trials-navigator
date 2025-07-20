# gene2trials_app.py

import streamlit as st
import pandas as pd

from utils.mutations import fetch_mutations
from utils.diseases import fetch_diseases
from utils.drugs import fetch_drugs_for_gene
from utils.trials import fetch_clinical_trials
from utils.summarizer import summarize_pubmed_abstracts

st.set_page_config(page_title="Gene2Trials Navigator", layout="wide")
st.title("🧬 Gene2Trials: Mutation → Drug Trial Navigator")

st.markdown("""
Enter a gene symbol (e.g., TP53, BRCA1) to explore associated mutations, diseases,
drugs, clinical trials, and AI-generated research summaries.
""")

gene_symbol = st.text_input("🔍 Enter Gene Symbol:", "TP53")

if gene_symbol:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Gene Mutations", "Associated Diseases", "Drugs", "Clinical Trials", "Research Summaries"])

    # 🧬 GENE MUTATIONS TAB
    with tab1:
        st.subheader("🧬 Gene Mutations")
        try:
            mutations = fetch_mutations(gene_symbol)

            if isinstance(mutations, list) and mutations and isinstance(mutations[0], dict):
                df_mut = pd.DataFrame(mutations)
                st.dataframe(df_mut)

                st.download_button(
                    label="📥 Download Mutations CSV",
                    data=df_mut.to_csv(index=False).encode('utf-8'),
                    file_name=f"{gene_symbol}_mutations.csv",
                    mime="text/csv"
                )
            else:
                st.write(mutations)

        except Exception as e:
            st.error(f"Error fetching mutations: {e}")

    # 🩠 ASSOCIATED DISEASES TAB
    with tab2:
        st.subheader("🩠 Associated Diseases")
        try:
            diseases = fetch_diseases(gene_symbol)
            st.write(diseases)
        except Exception as e:
            st.error(f"Error fetching diseases: {e}")

    # 💊 DRUGS TAB
    with tab3:
        st.subheader("💊 Drugs for Mutations")
        try:
            drugs = fetch_drugs_for_gene(gene_symbol)
            st.write(drugs)
        except Exception as e:
            st.error(f"Error fetching drugs: {e}")

    # 🧪 CLINICAL TRIALS TAB
    with tab4:
        st.subheader("🧪 Clinical Trials")
        try:
            trials = fetch_clinical_trials(gene_symbol)
            st.write(trials)
        except Exception as e:
            st.error(f"Error fetching trials: {e}")

    # 📚 RESEARCH SUMMARIES TAB
    with tab5:
        st.subheader("📚 Research Summaries")
        try:
            summaries = summarize_pubmed_abstracts(gene_symbol)
            for idx, item in enumerate(summaries):
                st.markdown(f"**{idx+1}. {item['title']}**")
                st.markdown(item['summary'])
        except Exception as e:
            st.error(f"Error generating summaries: {e}")
