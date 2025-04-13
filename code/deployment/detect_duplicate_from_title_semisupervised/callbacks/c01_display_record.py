from dash import Output, Input, html, callback

from code.deployment.detect_duplicate_from_title_semisupervised import BATCH_SIZE, df_full

callback(
    Output("record-display", "children"),
    Output("page-status", "children"),
    Input("current-index", "data"),
    Input("batch-start", "data")
)


def display_record(idx, batch_start):
    batch_end = batch_start + BATCH_SIZE
    if idx + batch_start >= len(df_full):
        return "End of dataset reached.", f"{idx + 1} / {min(batch_end, len(df_full))}"

    row = df_full.iloc[batch_start + idx]
    return html.Div([
        html.Strong(f"Record #{idx + 1 + batch_start}"),
        html.Div(f"Title 1: {row['title1']}"),
        html.Div(f"Title 2: {row['title2']}"),
        html.Div(f"Title Similarity: {row['title_similarity']:.3f}"),
        html.Div(f"Rule-based Label: {row.get('is_duplicate_rule_based', 'N/A')}")
    ]), f"{idx + 1 + batch_start} / {min(batch_end, len(df_full))}"
