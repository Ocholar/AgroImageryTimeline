import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

print("🔁 Starting Maize Yield Monitor...")

# Load data
df = pd.read_csv("data/yield_metrics.csv")

# Add outlier flags
df["Flag"] = df["YieldPerAcre"].apply(lambda y: "⚠️ Outlier" if y > 1200 or y < 300 else "")

# Start Dash app
app = dash.Dash(__name__)
app.title = "Maize Yield Monitor 🌽"

# Layout
app.layout = html.Div([
    html.H1("Maize Yield Monitor Dashboard 🌾", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Season", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="season-selector",
            options=[{"label": season, "value": season} for season in sorted(df["Season"].unique())],
            value=sorted(df["Season"].unique())[0]
        )
    ], style={"width": "40%", "margin": "auto"}),

    html.Br(),

    html.Div(id="summary-output", style={"textAlign": "center"}),

    html.Br(),

    html.Div([
        dcc.Graph(id="variety-leaderboard"),
        dcc.Graph(id="country-comparison"),
        dcc.Graph(id="quality-scatter")
    ]),

    html.Br(),

    html.Div(id="variety-table", style={"width": "60%", "margin": "auto", "textAlign": "center"}),

    html.Br(),

    html.P("⚠️ Outliers flagged when yield/acre >1200 or <300", style={"textAlign": "center", "color": "red"}),

    html.P("📥 CSV export and image preview coming soon!", style={"textAlign": "center", "fontStyle": "italic"})
])

# Summary card
@app.callback(
    Output("summary-output", "children"),
    Input("season-selector", "value")
)
def update_summary(selected_season):
    filtered = df[df["Season"] == selected_season]
    avg_yield = round(filtered["EstimatedYieldKG"].dropna().mean(), 2)
    avg_yield_per_acre = round(filtered["YieldPerAcre"].dropna().mean(), 2)
    sample_size = len(filtered)

    return html.Div([
        html.H3(f"📊 Summary for {selected_season}"),
        html.P(f"🧮 Avg Estimated Yield: {avg_yield} kg"),
        html.P(f"🌱 Avg Yield per Acre: {avg_yield_per_acre} kg/acre"),
        html.P(f"📦 Plots Sampled: {sample_size}")
    ])

# Variety leaderboard chart
@app.callback(
    Output("variety-leaderboard", "figure"),
    Input("season-selector", "value")
)
def update_variety_chart(selected_season):
    filtered = df[df["Season"] == selected_season]
    grouped = filtered.groupby("Variety")["YieldPerAcre"].mean().reset_index()
    grouped = grouped.sort_values("YieldPerAcre", ascending=False)

    fig = px.bar(grouped, x="Variety", y="YieldPerAcre",
                 title="🌾 Yield per Acre by Variety",
                 color="YieldPerAcre", labels={"YieldPerAcre": "kg/acre"})
    fig.update_layout(xaxis_title="Variety", yaxis_title="Yield per Acre")
    return fig

# Country comparison chart
@app.callback(
    Output("country-comparison", "figure"),
    Input("season-selector", "value")
)
def update_country_chart(selected_season):
    filtered = df[df["Season"] == selected_season]
    grouped = filtered.groupby("Country")["YieldPerAcre"].mean().reset_index()

    fig = px.bar(grouped, x="Country", y="YieldPerAcre",
                 title="🌍 Yield per Acre by Country",
                 color="YieldPerAcre", labels={"YieldPerAcre": "kg/acre"})
    fig.update_layout(xaxis_title="Country", yaxis_title="Yield per Acre")
    return fig

# Image quality vs yield scatter plot
@app.callback(
    Output("quality-scatter", "figure"),
    Input("season-selector", "value")
)
def update_quality_scatter(selected_season):
    filtered = df[df["Season"] == selected_season]

    fig = px.scatter(filtered, x="Quality", y="YieldPerAcre",
                     color="Variety", hover_data=["ImgID", "Flag"],
                     title="🎯 Image Quality vs Yield per Acre")
    fig.update_layout(xaxis_title="Image Quality", yaxis_title="Yield per Acre")
    return fig

# Variety comparison table
@app.callback(
    Output("variety-table", "children"),
    Input("season-selector", "value")
)
def update_variety_table(selected_season):
    filtered = df[df["Season"] == selected_season]
    grouped = filtered.groupby("Variety")["YieldPerAcre"].agg(["mean", "count"]).reset_index()
    grouped.columns = ["Variety", "AvgYieldPerAcre", "SampleSize"]
    grouped = grouped.sort_values("AvgYieldPerAcre", ascending=False)

    return html.Table([
        html.Tr([html.Th("Variety"), html.Th("Avg Yield/acre"), html.Th("Samples")])
    ] + [
        html.Tr([
            html.Td(row["Variety"]),
            html.Td(f"{row['AvgYieldPerAcre']:.2f}"),
            html.Td(row["SampleSize"])
        ]) for _, row in grouped.iterrows()
    ])

# Run server
if __name__ == "__main__":
    print("🚀 Launching Dash app...")
    app.run(debug=True)
