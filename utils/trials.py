def fetch_clinical_trials(gene_symbol):
    try:
        url = f"https://clinicaltrials.gov/api/query/study_fields?expr={gene_symbol}&fields=NCTId,BriefTitle,Condition,Phase,LocationCity,StartDate&min_rnk=1&max_rnk=20&fmt=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        studies = data.get("StudyFieldsResponse", {}).get("StudyFields", [])
        if not studies:
            return [{"trial": "No clinical trials found"}]

        trials = []
        for study in studies:
            trials.append({
                "NCT ID": study.get("NCTId", ["N/A"])[0],
                "Title": study.get("BriefTitle", ["N/A"])[0],
                "Condition": study.get("Condition", ["N/A"])[0],
                "Phase": study.get("Phase", ["N/A"])[0],
                "Start Date": study.get("StartDate", ["N/A"])[0]
            })

        return trials

    except Exception as e:
        return [{"trial": f"API request failed: {str(e)}"}]
