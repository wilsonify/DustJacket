
# 📚 DustJacket: Machine Learning-Powered Metadata Cleanup for Calibre

DustJacket brings the power of machine learning to your Calibre library. This project helps automatically clean, standardize, and enrich your `metadata.db` using a modular and scalable approach inspired by Microsoft’s Team Data Science Process (TDSP).

---

## 🧭 Introduction

[Calibre](https://calibre-ebook.com/) is an outstanding, open-source e-book management tool loved by readers and digital librarians. It allows users to organize, convert, and manage e-books across formats and devices.

However, as libraries grow, so does the **metadata chaos**.

### ⚠️ The Problem

Over time, Calibre’s metadata may suffer from:

- Inconsistent author name formats (e.g., *J.K. Rowling* vs *Rowling, J. K.*)
- Duplicates, typos, or missing fields
- Irregular or user-defined genres and tags

Manual cleanup is labor-intensive and error-prone. **Machine learning (ML)** can help by identifying patterns and recommending intelligent fixes.

---

## 💡 Core ML Concepts

### 1. Author Name Normalization

- **Technique**: TF-IDF + Clustering (DBSCAN) + Named Entity Recognition (NER)
- **Goal**: Group and normalize variations of author names
- **Example**: Combine `Rowling, J.K.` and `Joanne Rowling`

### 2. Genre/Tag Standardization

- **Technique**: NLP Classification (Logistic Regression or Transformers)
- **Inputs**: Title, description, or book content
- **Output**: Standardized genres like `"Science Fiction"`, `"Biography"`

### 3. Duplicate Detection

- **Technique**: Fuzzy matching (Levenshtein), cosine similarity
- **Goal**: Detect near-identical books by comparing titles + authors

### 4. Missing Metadata Imputation

- **Technique**: k-Nearest Neighbors or pretrained language models
- **Goal**: Predict missing fields like `series`, `publisher`, or `tags`

---

## ⚙️ How It Works: A Practical Workflow

### Step 1: Extract Metadata

```bash
sqlite3 metadata.db "SELECT title, authors, tags FROM books;"
```

Or use Python:

```python
import pandas as pd
import sqlite3
conn = sqlite3.connect("metadata.db")
df = pd.read_sql_query("SELECT * FROM books;", conn)
```

### Step 2: Clean Text

- Lowercase, strip punctuation
- Normalize whitespace and tokens
- Optionally, lemmatize or remove stopwords

### Step 3: Train & Apply ML Models

- Author clustering (`code/author_clustering.py`)
- Genre prediction (`code/genre_classifier.py`)
- Duplicate detection (`code/duplicate_detector.py`)

### Step 4: Review & Fix

- Generate a CSV with suggested corrections
- Apply them using Calibre’s `calibredb` CLI or API

---

## 📊 Visual Insights

- Author clustering (e.g., PCA-reduced scatter plots)
- Genre frequency bar charts
- Heatmaps of missing fields
- Similarity matrices for duplicates

---

## 🔁 Real-World Usage Pattern

```bash
Extract metadata.db → Analyze with ML → Generate corrections → Review → Re-import via Calibre tools
```

---

## 🌟 Bonus Ideas

- Fine-tune transformer models for better genre prediction
- Use OCR on covers to infer missing titles or genres
- Build a simple web interface for reviewing corrections
- Automate with scheduled jobs to clean new additions

---

## 📂 Project Structure (TDSP-Aligned)

```
DustJacket/
├── README.md
├── .gitignore
├── requirements.txt
├── setup.py
│
├── code/
│   ├── extract_metadata.py
│   ├── clean_text.py
│   ├── author_clustering.py
│   ├── genre_classifier.py
│   ├── duplicate_detector.py
│   └── apply_fixes.py
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   ├── 02-author-clustering.ipynb
│   └── 03-genre-classification.ipynb
│
├── outputs/
│   ├── reports/
│   └── predictions/
│
├── docs/
│   ├── tdsp_project_structure.md
│   ├── data_dictionary.md
│   └── modeling_decisions.md
│
└── tests/
    ├── test_extract_metadata.py
    └── test_duplicate_detection.py
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/calibre-ml-cleanup.git
cd calibre-ml-cleanup
pip install -r requirements.txt
```

---

## 🙌 Acknowledgments

- [Calibre](https://calibre-ebook.com/)
- [scikit-learn](https://scikit-learn.org/)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [TDSP Framework](https://learn.microsoft.com/en-us/azure/architecture/data-science-process/)