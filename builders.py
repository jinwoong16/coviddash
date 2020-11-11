import dash_html_components as html
import plotly.graph_objects as go
from data import make_global_df, make_country_df

color_spec = {
    'confirmed': '#e74c3c',
    'deaths': '#8e44ad',
    'recovered': '#27ae60'
}


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                style={"display": "block", "marginBottom": 25},
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontWeight": "600",
                            "fontSize": 16,
                        },
                        children=[
                            html.Th(column_name.replace("_", " ")) for column_name in df.columns
                        ]
                    )
                ]
            ),
            html.Tbody(
                style={"maxHeight": "50vh",
                       "display": "block", "overflow": "scroll"},
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "borderTop": "1px solid white",
                            "padding": "30px 0px",
                        },
                        children=[
                            html.Td(
                                value_column,
                                style={"textAlign": "center"}
                            ) for value_column in value
                        ]
                    ) for value in df.values
                ]
            )
        ]
    )


def make_graph(country=None):
    if country:
        df = make_country_df(country)
    else:
        df = make_global_df()
    fig = go.Figure()

    def make_scatter(case):
        fig.add_trace(go.Scatter(
            name=case,
            x=df['date'],
            y=df[case],
            hovertemplate=case + ': %{y:,}<extra></extra>',
            marker_color=color_spec[case],
        ))

    make_scatter('confirmed')
    make_scatter('deaths')
    make_scatter('recovered')

    fig.update_layout(hovermode="x", template="plotly_dark")
    fig.update_xaxes(rangeslider_visible=True)
    return fig
