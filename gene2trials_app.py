# gene2trials_app.py

import streamlit as st
import pandas as pd
from utils.mutations import fetch_mutations
from utils.diseases import fetch_diseases
from utils.drugs import fetch_drugs
from utils.trials import fetch_clinical_trials
from utils.lit_summary import fetch_pubmed_abstracts, summarize_text

st.set_page_config(page_title="Gene2Trials Navigator", layout="wide")
st.title("🧬 Gene2Trials: Mutation → Drug Trial Navigator")

# --- Input ---
gene_symbol = st.text_input("Enter a Gene Symbol (e.g., TP53, BRCA1)")

if gene_symbol:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧬 Mutations", "🧠 Diseases", "💊 Drugs", "🧪 Clinical Trials", "📚 AI Summary"
    ])

    # 🧬 GENE MUTATIONS TAB
    with tab1:
        st.subheader("🧬 Gene Mutations")

        try:
            mutations = fetch_mutations(gene_symbol)

            if isinstance(mutations, list) and mutations and isinstance(mutations[0], dict):
                df_mut = pd.DataFrame(mutations)

                # 🏷️ Add Risk Badge based on CADD score
                def risk_label(score):
                    try:
                        score = float(score)
                        if score >= 20:
                            return "🔴 High"
                        elif score >= 10:
                            return "🟡 Moderate"
                        else:
                            return "🟢 Low"
                    except:
                        return "N/A"

                df_mut["risk_level"] = df_mut["cadd_score"].apply(risk_label)

                st.dataframe(df_mut)

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

    # 🧠 DISEASES TAB
    with tab2:
        st.subheader("🧠 Associated Diseases")
        diseases = fetch_diseases(gene_symbol)
        st.write("\n".join(diseases))

    # 💊 DRUGS TAB
    with tab3:
        st.subheader("💊 Associated Drugs")
        drugs = fetch_drugs(gene_symbol)
        st.write("\n".join(drugs))

    # 🧪 CLINICAL TRIALS TAB
    with tab4:
        st.subheader("🧪 Related Clinical Trials")
        trials = fetch_clinical_trials(gene_symbol)

        if isinstance(trials, list) and trials and isinstance(trials[0], dict):
            df_trials = pd.DataFrame(trials)
            st.dataframe(df_trials)
            st.download_button(
                label="📅 Download Trials CSV",
                data=df_trials.to_csv(index=False).encode('utf-8'),
                file_name=f"{gene_symbol}_clinical_trials.csv",
                mime="text/csv"
            )
        else:
            st.write(trials)

    # 📚 AI LITERATURE SUMMARY TAB
    with tab5:
        st.subheader("📚 AI Summary of Latest Literature")
        abstracts = fetch_pubmed_abstracts(gene_symbol)
        if abstracts:
            full_text = " ".join(abstracts)
            summary = summarize_text(full_text)
            st.write(summary)
        else:
            st.write("No abstracts found for summarization.")
