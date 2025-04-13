import dash
from dash import html, dcc

# === Dash App ===
app = dash.Dash(__name__)
app.title = "Book Title Duplicate Labeler"

app.layout = html.Div([
    html.H2("Book Duplicate Labeling Tool (Batch of 10,000)"),
    html.Div(id="record-display", style={"padding": "20px", "fontSize": "18px"}),
    html.Div([
        html.Button("Duplicate", id="btn-dup", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Not Duplicate", id="btn-notdup", n_clicks=0),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Button("← Prev", id="prev-btn", n_clicks=0),
        html.Span(id="page-status", style={"margin": "0 15px"}),
        html.Button("Next →", id="next-btn", n_clicks=0),
    ], style={"marginBottom": "30px"}),

    html.Button("Save Batch", id="save-btn", n_clicks=0, style={"marginTop": "10px"}),
    html.Div(id="save-confirm", style={"marginTop": "15px", "color": "green"}),

    dcc.Store(id="current-index", data=0),
    dcc.Store(id="batch-start", data=0),
])

if __name__ == "__main__":
    app.run_server(debug=True)
