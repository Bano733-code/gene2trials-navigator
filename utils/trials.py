# utils/trials.py

import requests

def fetch_clinical_trials(gene_symbol):
    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": gene_symbol,
        "fields": "NCTId,BriefTitle,Condition,InterventionName,LocationCountry,Phase,OverallStatus",
        "min_rnk": 1,
        "max_rnk": 50,  # Increased from 5 to 50
        "fmt": "json"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        trials = data["StudyFieldsResponse"]["StudyFields"]
        trial_data = []

        for trial in trials:
            trial_data.append({
                "nct_id": trial.get("NCTId", ["N/A"])[0],
                "title": trial.get("BriefTitle", ["No title"])[0],
                "condition": trial.get("Condition", ["N/A"])[0],
                "intervention": trial.get("InterventionName", ["N/A"])[0],
                "country": trial.get("LocationCountry", ["N/A"])[0],
                "phase": trial.get("Phase", ["N/A"])[0],
                "status": trial.get("OverallStatus", ["N/A"])[0]
            })

        return trial_data

    except Exception as e:
        return [{"error": f"API request failed: {str(e)}"}]
