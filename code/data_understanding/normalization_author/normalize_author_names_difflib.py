"""
Normalize Author Name
- **Goal**: Group and normalize variations of author names
- **Example**: Combine Rowling, J.K. and Joanne Rowling
"""
import re
import sqlite3
from collections import defaultdict
from difflib import SequenceMatcher

# Optional: manually define known equivalences
MANUAL_MAPPINGS = {
    "rowling, j.k.": "joanne rowling",
    "j.k. rowling": "joanne rowling",
}


def normalize_name(name):
    """ normalize_name """
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)  # remove punctuation
    if ',' in name:
        parts = [part.strip() for part in name.split(',', 1)]
        name = f"{parts[1]} {parts[0]}"
    return ' '.join(name.split())  # remove duplicate spaces


def get_similarity(a, b):
    """ get_similarity """
    return SequenceMatcher(None, a, b).ratio()


def group_similar_names(names, threshold=0.85):
    """group_similar_names"""
    groups = []
    used = set()
    for name in names:
        if name in used:
            continue
        group = [name]
        used.add(name)
        for other in names:
            if other not in used and get_similarity(name, other) > threshold:
                group.append(other)
                used.add(other)
        groups.append(group)
    return groups


def main(calibre_db_path, dry_run=True):
    conn = sqlite3.connect(calibre_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()

    normalized = {aid: normalize_name(name) for aid, name in authors}

    # Apply manual overrides
    for aid, norm in normalized.items():
        if norm in MANUAL_MAPPINGS:
            normalized[aid] = MANUAL_MAPPINGS[norm]

    # Reverse mapping: norm_name -> list of author_ids
    rev_map = defaultdict(list)
    for aid, norm in normalized.items():
        rev_map[norm].append(aid)

    unique_norm_names = list(rev_map.keys())
    grouped = group_similar_names(unique_norm_names)

    print("=== Suggested Groups ===")
    for group in grouped:
        print(" -> ".join(group))

    if not dry_run:
        for group in grouped:
            canonical = group[0]
            for variant in group[1:]:
                for aid in rev_map[variant]:
                    print(f"Updating author ID {aid} to '{canonical}'")
                    cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (canonical.title(), aid))
        conn.commit()
        print("Database updated.")
    else:
        print("\n(Dry run - no changes made)")

    conn.close()

# Example usage:
# main('/path/to/Calibre Library/metadata.db', dry_run=True)
