import streamlit as st
from utils.mutations import fetch_mutations
from utils.diseases import fetch_diseases
from utils.drugs import fetch_drugs
from utils.trials import fetch_trials
from utils.summarizer import summarize_pubmed_abstracts

st.set_page_config(page_title="Gene2Trials: Mutation → Drug Trial Navigator", layout="wide")
st.title("🧬 Gene2Trials: Mutation → Drug Trial Navigator")

# Input field
gene_symbol = st.text_input("Enter Gene Symbol (e.g., TP53, BRCA1)", value="TP53")

if gene_symbol:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Gene Mutations", "Associated Diseases", "Drugs", "Clinical Trials", "Research Summaries"])

    with tab1:
        st.subheader("🧬 Gene Mutations")
        mutations = fetch_mutations(gene_symbol)
        if mutations:
            for mut in mutations:
                st.markdown(f"- {mut}")
        else:
            st.warning("No mutation data found.")

    with tab2:
        st.subheader("🦠 Associated Diseases")
        diseases = fetch_diseases(gene_symbol)
        if diseases:
            for d in diseases:
                st.markdown(f"- {d}")
        else:
            st.warning("No disease associations found.")

    with tab3:
        st.subheader("💊 Drugs Targeting This Gene")
        drugs = fetch_drugs(gene_symbol)
        if drugs:
            for drug in drugs:
                st.markdown(f"- {drug}")
        else:
            st.warning("No drugs found.")

    with tab4:
        st.subheader("🧪 Clinical Trials")
        trials = fetch_trials(gene_symbol)
        if trials:
            for trial in trials:
                st.markdown(f"- [{trial['title']}]({trial['url']})")
        else:
            st.warning("No clinical trials found.")

    with tab5:
        st.subheader("📚 AI-Generated PubMed Summaries")
        abstracts = summarize_pubmed_abstracts(gene_symbol)

        if not abstracts:
            st.warning("No summaries available for this gene.")
        else:
            for idx, item in enumerate(abstracts):
                st.markdown(f"### {idx + 1}. Summary")

                if isinstance(item, dict):
                    if 'title' in item:
                        st.markdown(f"**📝 Title:** {item['title']}")
                    if 'abstract' in item:
                        st.markdown(f"**📄 Abstract:** {item['abstract']}")
                    else:
                        st.markdown("Abstract not available.")
                elif isinstance(item, str):
                    st.write(item)
                else:
                    st.warning("Unsupported abstract format.")
