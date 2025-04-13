import csv
import json
import logging
import os
from glob import glob
from itertools import combinations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Paths ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../../../data")
INPUT_DIR = os.path.join(DATA_DIR, "input/books_metadata")
OUTPUT_DIR = os.path.join(DATA_DIR, "output_batches")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Batch Config ---
BATCH_SIZE = 10_000


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

    title1, title2 = extract_title(data1), extract_title(data2)

    return {
        "file1": os.path.basename(f1),
        "file2": os.path.basename(f2),
        "title1": title1,
        "title2": title2,
        "title_jaccard": jaccard_similarity(title1, title2),
        "title_cosine": cosine_sim(title1, title2),
        "is_duplicate_hand_labeled": ""  # to be filled manually
    }


# --- Main ---
def main():
    metadata_files = glob(os.path.join(INPUT_DIR, "*.json"))
    total_pairs = len(metadata_files) * (len(metadata_files) - 1) // 2
    logging.info(f"Found {len(metadata_files)} metadata files")
    logging.info(f"Total comparisons: {total_pairs}")

    batch_index = 0
    current_batch = []
    writer = None
    fieldnames = ["file1", "file2", "title1", "title2", "title_jaccard", "title_cosine", "is_duplicate_hand_labeled"]

    for i, (f1, f2) in enumerate(tqdm(combinations(metadata_files, 2), total=total_pairs, desc="Processing pairs")):
        row = process_pair(f1, f2)
        if not row:
            continue

        current_batch.append(row)

        if len(current_batch) >= BATCH_SIZE:
            batch_path = os.path.join(OUTPUT_DIR, f"book_similarity_batch_{batch_index}.csv")
            with open(batch_path, "w", encoding="utf-8", newline="") as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(current_batch)
            logging.info(f"Wrote batch {batch_index} with {len(current_batch)} records")
            current_batch = []
            batch_index += 1

    # Final batch
    if current_batch:
        batch_path = os.path.join(OUTPUT_DIR, f"book_similarity_batch_{batch_index}.csv")
        with open(batch_path, "w", encoding="utf-8", newline="") as out_csv:
            writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(current_batch)
        logging.info(f"Wrote final batch {batch_index} with {len(current_batch)} records")


if __name__ == "__main__":
    main()
