
# TDSP Project Structure: Calibre Metadata Cleanup with Machine Learning

This document describes how the **Calibre ML Cleanup** project applies the principles of the **Team Data Science Process (TDSP)** to develop a robust, modular, and scalable solution for automated metadata correction within Calibre libraries.

TDSP offers a structured lifecycle and folder organization for executing data science projects in a reproducible and collaborative manner. This framework guides our approach from business understanding through deployment and customer validation.

---

## 📌 Project Overview

**Objective**  
Use machine learning to intelligently clean and enrich Calibre's `metadata.db`, enabling users to:

- Normalize inconsistent author names
- Predict and standardize genres and tags
- Detect and merge duplicate entries
- Infer and populate missing metadata fields

**Target Audience**  
Calibre users and digital librarians managing large collections who require reliable, automated metadata consistency tools.

**Core Technologies**  
Python · SQLite · pandas · scikit-learn · fuzzywuzzy · HuggingFace Transformers (optional)

---

## 🧱 Repository Structure (TDSP-Aligned)

```bash
calibre-ml-cleanup/
├── code/                # Reusable modules for data access, processing, modeling, inference
├── data/
│   ├── raw/             # Exported metadata.db snapshots
│   ├── interim/         # Intermediate preprocessed versions
│   └── processed/       # Cleaned metadata files ready for application
├── docs/                # Project planning, modeling decisions, and documentation
├── notebooks/           # Interactive experiments and visualizations
├── outputs/             # Model outputs, logs, reports, predictions
├── tests/               # Unit and integration tests for core logic
├── README.md            # Project overview and usage
├── requirements.txt     # Python dependencies
└── setup.py             # CLI packaging and installation configuration
```

---

## 🔁 TDSP Lifecycle Alignment

### 1. 📈 Business Understanding

- **Scope**: Automate and streamline metadata correction in Calibre using machine learning.
- **Success Metrics**:
  - Accuracy of metadata predictions (e.g., author clustering, genre classification)
  - Reduction in manual correction time
  - Number of duplicate or incomplete entries resolved

📄 **See**: `docs/project_definition.md` (to be created)

---

### 2. 📊 Data Acquisition and Understanding

- **Source**: Calibre’s `metadata.db`, queried via SQLite
- **Tools**: `code/extract_metadata.py` parses the database into structured pandas DataFrames
- **Initial Exploration**: Conducted in `notebooks/01-data-exploration.ipynb`

📁 **See**:
- `data/raw/` — Original exported database snapshots  
- `docs/data_dictionary.md` — Schema and field definitions

---

### 3. 🤖 Modeling and Feature Engineering

- **Author Normalization**: DBSCAN clustering using TF-IDF embeddings
- **Genre Prediction**: Multiclass classifier trained on book descriptions (e.g., logistic regression, transformers)
- **Duplicate Detection**: Fuzzy matching on title-author pairs
- **Missing Field Imputation**: k-Nearest Neighbors and content similarity inference

📄 **See**:
- Scripts: `code/author_clustering.py`, `genre_classifier.py`, `duplicate_detector.py`
- Notebooks: `notebooks/02-author-clustering.ipynb`, `notebooks/03-genre-classification.ipynb`

---

### 4. 🚀 Deployment

- **Output Options**:
  - Export cleaned metadata to CSV/JSON
  - Apply changes using Calibre’s `calibredb` CLI
- **Planned Enhancements**:
  - Command-line interface (CLI) for automation
  - Interactive UI for human-in-the-loop review

📁 **See**:
- `code/apply_fixes.py`
- `outputs/predictions/` and `outputs/reports/`

---

### 5. ✅ Customer Acceptance

- **Validation Methods**:
  - Side-by-side comparison of before/after entries
  - Confidence scoring for suggested corrections
  - Backup/rollback options for changes
- **Documentation**: Visual summaries and model rationale

📄 **See**:
- `outputs/reports/cleanup_summary.md` (to be generated)
- `docs/modeling_decisions.md`

---

## 🧪 Reproducibility and Collaboration

- **Version Control**: Git & GitHub with pull requests and branching
- **Environment Management**: `requirements.txt` (Conda environment planned)
- **Modularity**: Pipeline stages separated by role (extract → clean → model → apply)
- **Testing**: `tests/` directory for core functions and regressions

---

## 🌱 Future Enhancements

- Deep learning for OCR-based genre classification from cover images
- Web-based dashboard for reviewing suggested metadata corrections
- Syncing with cloud-based Calibre libraries (e.g., Google Drive, OneDrive)
- Active learning loop with user feedback for model refinement

---

## 📚 References

- [Microsoft Team Data Science Process (TDSP)](https://learn.microsoft.com/en-us/azure/architecture/data-science-process/)
- [Calibre Database Schema](https://manual.calibre-ebook.com/db_structure.html)
- [FuzzyWuzzy Matching Library](https://github.com/seatgeek/thefuzz)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
