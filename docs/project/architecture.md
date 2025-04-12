

🏗️ architecture.md: DustJacket Calibre Plugin

    This document outlines the architecture and design of the DustJacket Calibre plugin—an integrated machine learning assistant for metadata cleanup and enhancement.

```mermaid
flowchart TD
    A[Calibre Plugin] --> B[DustJacket Calibre Plugin]
    B --> C[Plugin Entry Point<br>(__init__.py)]

    C --> D[MetadataController.py]
    C --> E[MLController.py]

    D --> F[Calibre Database]
    F --> G[Utilities]

    E --> H[author_clustering.py]
    E --> I[genre_classifier.py]
    E --> J[duplicate_detector.py]
    E --> K[impute_metadata.py]

    F --> E

```

📌 Purpose

DustJacket helps users analyze, standardize, and enhance Calibre metadata using machine learning directly inside the Calibre GUI or CLI. It supports:

    Author name normalization

    Genre/tag standardization

    Duplicate detection

    Missing field imputation

🧱 Plugin Architecture Overview

Calibre Plugin Runtime
│
├── Plugin Entry Point: __init__.py
│   └── GUI & CLI integration
│
├── Controllers
│   ├── MetadataController.py  ← interface to Calibre metadata
│   └── MLController.py        ← bridge to ML models
│
├── ML Modules (Imported)
│   ├── author_clustering.py
│   ├── genre_classifier.py
│   ├── duplicate_detector.py
│   └── impute_metadata.py
│
├── Utilities
│   ├── clean_text.py
│   ├── data_io.py
│   └── logging_utils.py
│
└── Resources
    ├── config.json
    └── pretrained_models/

🧭 Key Components Explained
1. __init__.py (Plugin Entry Point)

    Registers DustJacket as a Calibre plugin

    Adds menu options (GUI) or commands (CLI)

    Hooks into library_changed events to optionally run scans automatically

2. MetadataController.py

    Reads and writes to Calibre's database via Calibre API:

    db = self.gui.current_db
    mi = db.get_metadata(book_id)

    Normalizes internal representations for consistency

3. MLController.py

    Loads and interfaces with ML models (pretrained or on-demand)

    Accepts cleaned metadata as input

    Returns structured suggestions (e.g., fix recommendations or duplicates)

Example interface:

def suggest_fixes(book_batch: List[Metadata]) -> List[FixSuggestion]:
    ...

🧠 ML Processing Pipeline

The machine learning operations follow this staged workflow:

Extract metadata → Clean & vectorize → Apply ML models → Generate suggestions

🧪 Author Name Normalization

    Clustering Algorithm: DBSCAN on TF-IDF vectors of author names

    NER: Used to refine canonical names (e.g., "Joanne Rowling")

🗂️ Genre Standardization

    Input: Title, description

    Model: Logistic Regression or Transformer fine-tuned on genre-tagged corpora

    Output: Calibre-compatible tags

🧬 Duplicate Detection

    Similarity: Cosine or Levenshtein between normalized title + author

    Thresholding: Tunable confidence for "soft" or "hard" matches

🔍 Missing Field Prediction

    k-NN or BERT-style embeddings (title/context-based)

    Predicts series, publisher, or tags from similar entries

🧰 Data Flow Example

User clicks “Analyze Metadata”
↓
Calibre passes book metadata to MetadataController
↓
Cleaned and vectorized data forwarded to MLController
↓
Model predictions returned (e.g., fix suggestions)
↓
User reviews in a GUI panel or exports results
↓
User applies changes via Calibre API or `calibredb`

📦 Plugin Modes
🔹 Interactive (GUI)

    Triggered via toolbar or right-click

    Opens a modal for:

        Review of model suggestions

        One-click apply or export

🔸 Batch (CLI)

calibredb run_dustjacket --fix-authors --detect-duplicates

    Useful for automation, CI/CD for libraries, or large-scale cleanup

🔁 Extensibility
✅ Modular ML components:

    Swap out models (e.g., upgrade to LLMs or more robust clusterers)

    Hot-reload updated models via plugin settings

✅ External data integration:

    Optional: link to ISBN/Google Books/LOC APIs for metadata enrichment

✅ Web Dashboard (Future)

    Serve a lightweight Flask interface for advanced users:

        Review suggestions

        Compare versions

        Schedule automatic cleanups

🔒 Security & Performance

    All processing happens locally

    Plugin avoids external I/O unless configured explicitly

    Models use caching for fast inference on repeated runs

    Supports incremental processing (only new/changed entries)

✅ Assumptions & Constraints

    Plugin operates on the metadata.db accessed via Calibre’s Python API

    Models trained or fine-tuned on representative ebook data (custom corpora ideal)

    Uses lightweight ML where feasible; heavier models are optional

📈 Suggested Improvements

    Model confidence scores for each suggestion

    Training mode to fine-tune genre prediction with user-labeled books

    ML model performance monitoring dashboard

🔚 Summary

DustJacket’s plugin architecture blends Calibre’s extensibility with machine learning intelligence, making metadata cleanup a repeatable, intelligent, and user-friendly task. It is designed to grow with your library—and with advances in NLP and ML tooling.