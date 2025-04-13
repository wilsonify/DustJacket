import dash
from dash import Output, Input, State, callback

from code.deployment.detect_duplicate_from_title_semisupervised import df_full

callback(
    Output("current-index", "data"),
    Input("btn-dup", "n_clicks"),
    Input("btn-notdup", "n_clicks"),
    State("current-index", "data"),
    State("batch-start", "data"),
)


def label_data(n_dup, n_notdup, idx, batch_start):
    ctx = dash.callback_context
    if not ctx.triggered:
        return idx

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    label = 1 if button_id == "btn-dup" else 0
    df_full.at[batch_start + idx, "is_duplicate_hand_labeled"] = label

    return idx + 1 if (batch_start + idx + 1) < len(df_full) else idx
