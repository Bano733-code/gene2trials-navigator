# 📁 utils/trials.py
import requests

def fetch_clinical_trials(gene_symbol):
    try:
        url = f"https://clinicaltrials.gov/api/query/study_fields?expr={gene_symbol}&fields=NCTId,Condition,BriefTitle,LeadSponsorName&min_rnk=1&max_rnk=20&fmt=json"
        res = requests.get(url)
        res.raise_for_status()
        trials = res.json()['StudyFieldsResponse']['StudyFields']

        results = []
        for trial in trials:
            results.append({
                "nct_id": trial.get("NCTId", ["N/A"])[0],
                "condition": ", ".join(trial.get("Condition", ["N/A"])),
                "title": trial.get("BriefTitle", ["N/A"])[0],
                "sponsor": trial.get("LeadSponsorName", ["N/A"])[0]
            })

        return results
    except Exception as e:
        return f"Error fetching trials: {e}"
