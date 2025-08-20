import requests
import pandas as pd
import streamlit as st

def fetch_clinical_trials(gene_symbol, page_size=20):
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.term": gene_symbol,
        "fields": (
            "protocolSection.identificationModule.nctId,"
            "protocolSection.identificationModule.briefTitle,"
            "protocolSection.conditionsModule.conditions,"
            "protocolSection.sponsorCollaboratorsModule.leadSponsor.name,"
            "protocolSection.statusModule.overallStatus"
        ),
        "pageSize": page_size
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        studies = resp.json().get("studies", [])
        results = []
        for study in studies:
            pf = study.get("protocolSection", {})
            id_mod = pf.get("identificationModule", {})
            cond_mod = pf.get("conditionsModule", {})
            stat_mod = pf.get("statusModule", {})
            sponsor_mod = pf.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})

            results.append({
                "nct_id": id_mod.get("nctId", ""),
                "title": id_mod.get("briefTitle", ""),
                "condition": ", ".join(cond_mod.get("conditions", [])),
                "sponsor": sponsor_mod.get("name", ""),
                "overall_status": stat_mod.get("overallStatus", "N/A")
            })
        return results
    except Exception as e:
        return f"Error fetching trials: {e}"

        
def status_badge(status):
    """Return emoji badge for clinical trial status"""
    s = status.lower()
    if "completed" in s:
        return "🟢 Completed"
    elif "recruiting" in s:
        return "🟡 Recruiting"
    elif "terminated" in s:
        return "🔴 Terminated"
    else:
        return "⚪ " + status

def render_trials_ui(gene_symbol: str):
    """Render clinical trials in Streamlit"""
    trials = fetch_clinical_trials(gene_symbol, page_size=15)

    if isinstance(trials, str):
        st.error(trials)
        return
    
    if not trials:
        st.warning("⚠️ No clinical trials found for this gene.")
        return

    df = pd.DataFrame(trials)
    df["NCT ID"] = df["nct_id"].apply(
        lambda x: f'<a href="https://clinicaltrials.gov/study/{x}" target="_blank">{x}</a>' if x else ""
    )
    # Clickable NCT links
    #df["NCT ID"] = df["nct_id"].apply(
     #   lambda x: f"[{x}](https://clinicaltrials.gov/study/{x})" if x else ""
    #)

    df = df.rename(columns={
        "title": "Title",
        "condition": "Condition",
        "sponsor": "Sponsor",
        "overall_status": "Status"
    })

    df_display = df[["NCT ID", "Title", "Condition", "Sponsor", "Status"]]
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    #st.dataframe(df, use_container_width=True)
    st.download_button(
        label="📥 Download Trials CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"{gene_symbol}_trials.csv",
        mime="text/csv")
