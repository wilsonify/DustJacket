# TDSP Project Structure: Calibre Metadata Cleanup with Machine Learning

This document outlines how the **Calibre ML Cleanup** project adheres to the principles of the **Team Data Science Process (TDSP)**. The TDSP provides a structured lifecycle and folder organization for collaborative, scalable, and reproducible data science projects.

---

## 📌 Project Overview

**Goal:**  
To automate the cleanup and enrichment of Calibre's `metadata.db` using machine learning techniques. This includes:
- Normalizing author names
- Predicting consistent genres and tags
- Detecting duplicates
- Filling in missing metadata fields

**Target Users:**  
Anyone managing large Calibre libraries who needs intelligent metadata correction and consistency.

**Primary Tools:**  
Python, SQLite, scikit-learn, pandas, fuzzywuzzy, HuggingFace Transformers (optional)

---

## 🧱 TDSP Directory Structure

```bash
calibre-ml-cleanup/
├── code/                # Scripts and modules for data access, cleaning, ML, and inference
├── data/                # Placeholder for datasets (raw, interim, and processed)
├── docs/                # Planning documents, data dictionary, and modeling decisions
├── notebooks/           # Interactive analysis and experimentation
├── outputs/             # Generated reports, model predictions, and evaluation results
├── tests/               # Unit and integration tests
├── README.md            # Overview of the project
├── requirements.txt     # Python package dependencies
└── setup.py             # Installation and CLI packaging
