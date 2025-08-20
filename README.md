# 🧬 Gene2Trials Navigator

Gene2Trials Navigator is a **Streamlit web app** that allows users to explore gene-related biomedical knowledge.  
Given a gene symbol (e.g., **TP53**, **BRCA1**), the app fetches **mutations, diseases, drugs, and clinical trials** from public biomedical APIs and provides **AI-powered summaries**.

---

## 🚀 Features
- 🔍 **Gene Mutations**: Extract mutations, CADD scores, and clinical significance using **MyVariant.info** / ClinVar.
- 🧪 **Associated Diseases**: Discover diseases linked to mutations.
- 💊 **Drug Information**: Retrieve drug candidates via **ChEMBL**.
- 📊 **Clinical Trials**: Get live data from **ClinicalTrials.gov**.
- 📝 **AI Summarization**: Summarize PubMed abstracts with Hugging Face Transformers.
- ✅ **Clickable Links**: Direct links to variants, drugs, and trial pages.

---

## 🛠️ Tech Stack
- **Languages**: Python
- **Frameworks**: Streamlit
- **APIs**:
  - [MyVariant.info](https://myvariant.info/)
  - [ChEMBL](https://www.ebi.ac.uk/chembl/)
  - [ClinicalTrials.gov](https://clinicaltrials.gov/)
  - [PubMed / Entrez](https://www.ncbi.nlm.nih.gov/)
- **AI Models**: HuggingFace Transformers
- **Deployment**: Hugging Face Spaces / GitHub

---
streamlit run app.py

📝 Usage
Enter a gene symbol (e.g., TP53).
Navigate tabs:
🦠 Mutations
🧬 Diseases
💊 Drugs
📋 Clinical Trials
📝 Summaries
Click on IDs to open external references.

📂 Project Structure
gene2trials-navigator/
│── app.py              # Main Streamlit app
│── utils/
│    ├── mutations.py   # MyVariant/ClinVar fetch
│    ├── diseases.py    # Disease associations
│    ├── drugs.py       # ChEMBL fetch
│    ├── trials.py      # ClinicalTrials.gov fetch
│    └── summaries.py   # PubMed summarization
│── requirements.txt
│── README.md
🤝 Contributing

PRs are welcome! If you find a bug, please open an issue.
## 📦 Installation
```bash
git clone https://github.com/Bano733-code/gene2trials-navigator.git
cd gene2trials-navigator
pip install -r requirements.txt```
