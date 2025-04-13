import os

from dash import Output, Input, State

from code.deployment.detect_duplicate_from_title_semisupervised import BATCH_SIZE
from code.deployment.detect_duplicate_from_title_semisupervised.__main__ import app


@app.callback(
    Output("save-confirm", "children"),
    Input("save-btn", "n_clicks"),
    State("batch-start", "data")
)
def save_labeled_batch(n_clicks, batch_start):
    if n_clicks > 0:
        batch_df = df_full.iloc[batch_start:batch_start + BATCH_SIZE]
        if os.path.exists(OUTPUT_PATH):
            batch_df.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)
        else:
            batch_df.to_csv(OUTPUT_PATH, index=False)
        return f"Saved batch {batch_start} - {batch_start + BATCH_SIZE}"
    return ""
