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

## 📂 Project Structure

```text
gene2trials-navigator/
│
├── app.py                         # Main Streamlit application
│
├── utils/
│   ├── mutations.py               # MyVariant & ClinVar mutation retrieval
│   ├── diseases.py                # Disease association analysis
│   ├── drugs.py                   # ChEMBL drug information retrieval
│   ├── trials.py                  # ClinicalTrials.gov trial search
│   └── summaries.py               # PubMed research paper summarization
│
├── requirements.txt               # Python dependencies
│
└── README.md                      # Project documentation
```

## 🤝 Contributing

Contributions are welcome!  

If you would like to improve Gene2Trials Navigator:

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

Please ensure your code follows clean structure and includes proper documentation.

## 📦 Installation
```bash
git clone https://github.com/Bano733-code/gene2trials-navigator.git
cd gene2trials-navigator
pip install -r requirements.txt```
