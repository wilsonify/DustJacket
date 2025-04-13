import dash
from dash import Output, Input, State, callback

from code.deployment.detect_duplicate_from_title_semisupervised import df_full

callback(
    Output("current-index", "data"),
    Output("batch-start", "data"),
    Input("prev-btn", "n_clicks"),
    Input("next-btn", "n_clicks"),
    State("current-index", "data"),
    State("batch-start", "data")
)


def paginate(n_prev, n_next, idx, batch_start):
    ctx = dash.callback_context
    if not ctx.triggered:
        return idx, batch_start

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "prev-btn" and idx > 0:
        return idx - 1, batch_start
    elif button_id == "next-btn" and (batch_start + idx + 1) < len(df_full):
        return idx + 1, batch_start
    return idx, batch_start
