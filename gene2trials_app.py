import streamlit as st
import pandas as pd
import requests
import re
from utils.mutations import fetch_mutations
from utils.diseases import fetch_diseases
from utils.drugs import fetch_drugs_for_gene
from utils.trials import fetch_clinical_trials
from utils.summarizer import fetch_pubmed_abstracts, summarize_text
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

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

    # 🦠 GENE MUTATIONS TAB
    with tab1:
        st.subheader("🦠 Gene Mutations")

        try:
            mutations = fetch_mutations(gene_symbol)

            if isinstance(mutations, list) and mutations and isinstance(mutations[0], dict):
                df_mut = pd.DataFrame(mutations)
                df_mut.sort_values(by="cadd_score", ascending=False, inplace=True)

                st.markdown(df_mut.to_html(escape=False, index=False), unsafe_allow_html=True)


                st.download_button(
                    label="📅 Download Mutations CSV",
                    data=df_mut.to_csv(index=False).encode('utf-8'),
                    file_name=f"{gene_symbol}_mutations.csv",
                    mime="text/csv"
                )
            else:
                st.write(mutations)

        except Exception as e:
            st.error(f"Error fetching mutations: {e}")

    # �� ASSOCIATED DISEASES TAB
    with tab2:
        st.subheader("�� Associated Diseases")
        try:
            diseases = fetch_diseases(gene_symbol)
            if isinstance(diseases, list) and isinstance(diseases[0], dict):
                df_disease = pd.DataFrame(diseases)
                 # Format numeric scores to 2 decimal places
                
                st.markdown(df_disease.to_markdown(index=False), unsafe_allow_html=True)

                st.download_button(
                    label="📅 Download Diseases CSV",
                    data=df_disease.to_csv(index=False).encode('utf-8'),
                    file_name=f"{gene_symbol}_diseases.csv",
                    mime="text/csv"
                )
            else:
                st.warning(diseases if isinstance(diseases, str) else "No diseases found.")
        except Exception as e:
            st.error(f"Error fetching diseases: {e}")

    # 💊 DRUGS TAB
    with tab3:
        st.subheader("💊 Drugs for Mutations")
        try:
            df_drugs = fetch_drugs_for_gene(gene_symbol)
             # Agar fallback dict ya dataframe se aa raha ho
            if isinstance(df_drugs, list):  # fallback list of dicts
                import pandas as pd
                df_drugs = pd.DataFrame(df_drugs)
            # Show unique sources if available
            if not df_drugs.empty:
                st.markdown(f"**Data for gene:** {gene_symbol}")
                df_display = df_drugs.dropna(axis=1, how="all")
                if "Approval" in df_display.columns:
                    approval_map = {
                        "0": "Preclinical",
                        "1": "Phase 1",
                        "2": "Phase 2",
                        "3": "Phase 3",
                        "4": "Approved"
                   }
                    df_display["Approval"] = (
                        df_display["Approval"].astype(str).map(approval_map).fillna(df_display["Approval"]))

                 # ✅ Ensure clean clickable IDs for BOTH fallback + API
                if "ID" in df_display.columns:
                    def make_clickable(x):
                        if pd.isna(x):
                            return "N/A"
                    # Remove any existing markdown around IDs like [CHEMBL1234](url)
                        plain_id = re.sub(r"^\[?([A-Z0-9]+)\]?.*$", r"\1", str(x))
                        return f"[{plain_id}](https://www.ebi.ac.uk/chembl/compound_report_card/{plain_id}/)"

                    df_display["ID"] = df_display["ID"].apply(make_clickable)
    # Show styled dataframe with clickable links
                st.markdown(df_display.to_markdown(index=False), unsafe_allow_html=True)

                # 🔹 Show sources used
                if "Source" in df_drugs.columns:
                    st.markdown("**Sources used:** " + ", ".join(df_drugs["Source"].dropna().unique()))

                #st.markdown("**Sources used:** " + ", ".join(df_drugs["Source"].unique()))
                st.download_button(
                    label="📅 Download Drugs CSV",
                    data=df_drugs.to_csv(index=False).encode('utf-8'),
                    file_name=f"{gene_symbol}_drugs.csv",
                    mime="text/csv"
                )

            else:
                st.warning("No drug data found.")
        except Exception as e:
            st.error(f"Error fetching drugs: {e}")

    # 🤪 CLINICAL TRIALS TAB
    with tab4:
        st.subheader("🔍 Clinical Trials")
        from utils.trials import render_trials_ui
        render_trials_ui(gene_symbol)


    # 📚 RESEARCH SUMMARIES TAB
    with tab5:
        st.subheader("📚 Research Summaries")
        try:
            abstracts = fetch_pubmed_abstracts(gene_symbol)
            summaries = [summarize_text(a["title"] + ". " + a["abstract"]) for a in abstracts]

            for i, summary in enumerate(summaries):
                st.markdown(f"**{i+1}. {abstracts[i]['title']}**")
                st.markdown(summary)

        except Exception as e:
            st.error(f"Error generating summaries: {e}")
