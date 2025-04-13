import json
import os
import csv
from glob import glob
from itertools import combinations
from typing import Tuple

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
OUTPUT_CSV = os.path.join(DATA_DIR, "output_actual/detect_duplicate_from_title.csv")


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


def extract_title(data: dict) -> str:
    return data.get("title", "")


def process_pair(f1: str, f2: str) -> dict:
    data1, data2 = safe_load_json(f1), safe_load_json(f2)
    if not data1 or not data2:
        return {}

    title1 = extract_title(data1)
    title2 = extract_title(data2)

    title_jaccard = jaccard_similarity(title1, title2)
    title_cosine = cosine_sim(title1, title2)

    return {
        "file1": os.path.basename(f1),
        "file2": os.path.basename(f2),
        "title1": title1,
        "title2": title2,
        "title_jaccard": title_jaccard,
        "title_cosine": title_cosine,
        "is_duplicate_rule_based": int(title_jaccard > 0.9)
    }


def main():
    metadata_files = glob(os.path.join(INPUT_DIR, "*.json"))
    total_pairs = len(metadata_files) * (len(metadata_files) - 1) // 2

    logging.info(f"Found {len(metadata_files)} metadata files")
    logging.info(f"Total comparisons: {total_pairs}")

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline='') as out_csv:
        writer = None
        for f1, f2 in tqdm(combinations(metadata_files, 2), total=total_pairs, desc="Comparing titles"):
            row = process_pair(f1, f2)
            if not row:
                continue

            if writer is None:
                writer = csv.DictWriter(out_csv, fieldnames=row.keys())
                writer.writeheader()

            writer.writerow(row)

    logging.info(f"Saved dataset to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
