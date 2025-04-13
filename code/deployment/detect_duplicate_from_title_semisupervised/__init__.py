# === Configuration ===
import pandas as pd

DATA_PATH = "../../../data/output_actual/detect_duplicate_from_title.csv"
BATCH_SIZE = 10000
OUTPUT_PATH = "../../../data/output_actual/labeled_detect_duplicate_from_title.csv"

# === Load Data ===
df_full = pd.read_csv(DATA_PATH)
df_full["is_duplicate_hand_labeled"] = df_full["is_duplicate_rule_based"]
