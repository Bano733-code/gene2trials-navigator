import requests

def get_clinical_trials(gene):
    url = f"https://clinicaltrials.gov/api/query/study_fields?expr={gene}&fields=NCTId,BriefTitle&min_rnk=1&max_rnk=10&fmt=json"
    try:
        res = requests.get(url).json()
        studies = res["StudyFieldsResponse"]["StudyFields"]
        return [{ "NCT ID": s["NCTId"][0], "Title": s["BriefTitle"][0] } for s in studies if s["NCTId"]]
    except:
        return []
