import json
import os
from glob import glob
from itertools import combinations
from typing import Tuple, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import logging

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Paths ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../../data")
INPUT_DIR = os.path.join(DATA_DIR, "input/books_metadata")
OUTPUT_CSV = os.path.join(DATA_DIR, "output_actual/book_similarity_dataset.csv")


# --- Utility Functions ---

def jaccard_similarity(a: str, b: str) -> float:
    set_a, set_b = set(a.lower().split()), set(b.lower().split())
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def cosine_sim(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer()
    try:
        vecs = vectorizer.fit_transform([text1, text2])
        return cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
    except ValueError:
        return 0.0


def safe_load_json(filepath: str) -> dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"Failed to load {filepath}: {e}")
        return {}


def extract_fields(data: dict) -> Tuple[str, str, List[str], str]:
    return (
        data.get("title", ""),
        data.get("author_name", ""),
        data.get("tags", []),
        data.get("description", "")
    )


def process_pair(f1: str, f2: str) -> dict:
    data1, data2 = safe_load_json(f1), safe_load_json(f2)

    title1, author1, tags1, desc1 = extract_fields(data1)
    title2, author2, tags2, desc2 = extract_fields(data2)

    return {
        "file1": os.path.basename(f1),
        "file2": os.path.basename(f2),
        "title1": title1,
        "title2": title2,
        "author1": author1,
        "author2": author2,
        "tags1": tags1,
        "tags2": tags2,
        "desc1": desc1,
        "desc2": desc2,
        "title_similarity": jaccard_similarity(title1, title2),
        "author_similarity": jaccard_similarity(author1, author2),
        "description_similarity": cosine_sim(desc1, desc2) if desc1 and desc2 else 0.0,
        "tag_similarity": jaccard_similarity(" ".join(tags1), " ".join(tags2)) if tags1 and tags2 else 0.0,
    }


def main():
    metadata_files = glob(os.path.join(INPUT_DIR, "*.json"))
    total_pairs = len(metadata_files) * (len(metadata_files) - 1) // 2

    logging.info(f"Found {len(metadata_files)} metadata files")
    logging.info(f"Total comparisons: {total_pairs}")

    results = []
    for f1, f2 in tqdm(combinations(metadata_files, 2), total=total_pairs, desc="Processing pairs"):
        row = process_pair(f1, f2)
        # Simple rule-based label
        row["is_duplicate_rule_based"] = int(row["title_similarity"] > 0.9 and row["author_similarity"] > 0.9)
        results.append(row)

    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    logging.info(f"Saved dataset with {len(df)} pairs to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
