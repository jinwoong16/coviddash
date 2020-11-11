import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
from builders import make_table, make_graph

stylesheet = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server

bubble_map = px.scatter_geo(countries_df,
                            title="Confirmed Cases By Country",
                            size="Confirmed",
                            size_max=40,
                            template="plotly_dark",
                            projection="natural earth",
                            color_continuous_scale=px.colors.sequential.Oryel,
                            hover_data={
                                "Confirmed": ":,2f",
                                "Deaths": ":,2f",
                                "Recovered": ":,2f",
                                "Country_Region": False
                            },
                            hover_name="Country_Region",
                            color="Confirmed",
                            locations="Country_Region",
                            locationmode="country names"
                            )

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

bars_graph = px.bar(totals_df,
                    title="Total Global Cases",
                    x="condition",
                    y="count",
                    template="plotly_dark",
                    hover_data={
                        'count': ":,"
                    },
                    labels={
                        'condition': 'Condition',
                        'count': 'Count',
                        'color': 'Condition'
                    }
                    )

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#121212",
        "color": "#C8D6E5",
        "fontFamily": "Roboto, sans-serif"
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "paddingTop": "50px",
                "marginBottom": 100
            },
            children=[html.H1("Global Status of COVID-19",
                              style={"fontSize": 50})]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"gridColumn": "span 3"},
                    children=[
                        dcc.Graph(figure=bubble_map)
                    ]
                ),
                html.Div(
                    children=[
                        make_table(countries_df)
                    ]
                ),
            ]
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    children=[
                        dcc.Graph(figure=bars_graph)
                    ]
                ),
                html.Div(
                    style={"gridColumn": "span 3"},
                    children=[
                        dcc.Dropdown(style={
                            "width": 320,
                            "margin": "0 auto",
                            "color": "#111111",
                        },
                            id="country",
                            options=[
                            {'label': country, 'value': country} for country in dropdown_options
                        ]),
                        dcc.Graph(id="country_graph")
                    ]
                )
            ]
        )
    ],
)


@app.callback(
    Output("country_graph", "figure"),
    [
        Input("country", "value")
    ]
)
def update_figure(value):
    return make_graph(value)


if __name__ == '__main__':
    app.run_server(debug=True)
