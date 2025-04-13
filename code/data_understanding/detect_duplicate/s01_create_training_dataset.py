import json
import os
from glob import glob
from itertools import combinations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

path_to_here = os.path.abspath(os.path.dirname(__file__))
path_to_data = os.path.abspath(f"{path_to_here}/../../../data")


# Utility functions
def jaccard_similarity(a: str, b: str) -> float:
    set_a, set_b = set(a.lower().split()), set(b.lower().split())
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def cosine_sim(text1: str, text2: str) -> float:
    vec = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(vec[0:1], vec[1:2])[0][0]


def main():
    # Setup paths
    metadata_files = glob(f"{path_to_data}/input/books_metadata/*.json")

    # For reproducibility and avoiding self-comparisons
    file_pairs = combinations(metadata_files, 2)

    # Store results
    rows = []
    for f1, f2 in file_pairs:
        with open(f1, 'r', encoding='utf-8') as file1, open(f2, 'r', encoding='utf-8') as file2:
            try:
                data1 = json.load(file1)
                data2 = json.load(file2)
            except Exception as e:
                print(f"Skipping pair ({f1}, {f2}) due to error: {e}")
                continue

        # Extract relevant fields
        title1, title2 = data1.get("title", ""), data2.get("title", "")
        author1, author2 = data1.get("author_name", ""), data2.get("author_name", "")
        tags1, tags2 = data1.get("tags", []), data2.get("tags", [])
        desc1, desc2 = data1.get("description", ""), data2.get("description", "")

        # Compute similarities
        title_sim = jaccard_similarity(title1, title2)
        author_sim = jaccard_similarity(author1, author2)
        desc_sim = cosine_sim(desc1, desc2) if desc1 and desc2 else 0.0
        tag_sim = jaccard_similarity(" ".join(tags1), " ".join(tags2)) if tags1 and tags2 else 0.0

        # Example placeholder label (for supervised learning this would be hand-labeled or rule-based)
        is_duplicate = int(title_sim > 0.9 and author_sim > 0.9)

        # Append row
        rows.append({
            "file1": os.path.basename(f1),
            "file2": os.path.basename(f2),
            "title1":title1,
            "title2":title2,
            "author1":author1,
            "author2":author2,
            "tags1":tags1,
            "tags2":tags2,
            "desc1":desc1,
            "desc2":desc2,
            "title_similarity": title_sim,
            "author_similarity": author_sim,
            "description_similarity": desc_sim,
            "tag_similarity": tag_sim,
            "is_duplicate_rule_based": is_duplicate
        })

    # Convert to DataFrame and save
    df = pd.DataFrame(rows)
    output_csv = os.path.join(path_to_data, f"{path_to_data}/output_actual/book_similarity_dataset.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"Saved dataset with {len(df)} pairs to {output_csv}")


if __name__ == "__main__":
    main()
