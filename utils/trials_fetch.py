# utils/trials.py

import requests

def fetch_clinical_trials(gene_symbol):
    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": gene_symbol,
        "fields": "NCTId,BriefTitle,Condition,InterventionName,LocationCountry",
        "min_rnk": 1,
        "max_rnk": 5,
        "fmt": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        trials = data["StudyFieldsResponse"]["StudyFields"]
        trial_data = []

        for trial in trials:
            trial_data.append({
                "nct_id": trial.get("NCTId", ["N/A"])[0],
                "title": trial.get("BriefTitle", ["No title"])[0],
                "condition": trial.get("Condition", ["N/A"])[0],
                "intervention": trial.get("InterventionName", ["N/A"])[0],
                "country": trial.get("LocationCountry", ["N/A"])[0]
            })

        return trial_data
    except Exception as e:
        return [{"error": str(e)}]
