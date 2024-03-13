import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

df1 = pd.read_csv('website/data/PM25_predictions/PM25_Songkhla.csv')

external_stylesheets = [
    {
        "href": "/static/css/style2.css",
        "rel": "stylesheet",
    },
]

def create_prediction_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", external_stylesheets=external_stylesheets, url_base_pathname="/prediction/")

    dash_app.title = "Happy Air Quality Prediction"
    dash_app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.Section(
                        className="breadcrumbs",
                        children=[
                            html.Div(
                                className="container",
                                children=[
                                    html.Div(
                                        className="d-flex justify-content-between align-items-center",
                                        children=[
                                            html.Ol(
                                                children=[
                                                    html.Li(html.A("Home", href="/")),
                                                    html.Li("Prediction")
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    html.P(children="🌏", className="header-emoji"),
                    html.H1(
                        children="Happy Air Quality Prediction", className="header-title"
                    ),
                    html.P(
                        children="Pycaret Time Series Module",
                        className="header-description",
                    ),
                    html.P(
                        children="Prediction in the next 7 days",
                        className='header-date'
                    ),
                    html.P(
                        children="Southern Thailand",
                        className='header-location'
                    ),
                ],
                className="header",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="Province", className="menu-title"),
                            dcc.Dropdown(
                                id="data",
                                options=[
                                    {"label": "Songkhla", "value": "Songkhla"},
                                    {"label": "Mueang, Yala", "value": "Mueang_Yala"},
                                    {"label": "Betong, Yala", "value": "Betong_Yala"},
                                    {"label": "Nakhon Si Thammarat", "value": "Nakhon_Si_Thammarat"},
                                    {"label": "Narathiwat", "value": "Narathiwat"},
                                    {"label": "Phuket", "value": "Phuket"},
                                    {"label": "Satun", "value": "Satun"},
                                    {"label": "Surat Thani", "value": "Surat_Thani"},
                                    {"label": "Trang", "value": "Trang"},
                                ],
                                value="Songkhla",
                                clearable=False,
                                className="dropdown-data",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(children="Parameter", className="menu-title"),
                            dcc.Dropdown(
                                id="parameter-filter",
                                options=[
                                    {"label": "PM25", "value": "PM25"},
                                    {"label": "TEMP", "value": "TEMP"},
                                    {"label": "RH", "value": "RH"},
                                ],
                                value="PM25",
                                clearable=False,
                                className="dropdown-parameter",
                            ),
                        ]
                    ),
                ],
                className="menu",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id="air-quality-chart", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                    html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="daily-stats", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
                    
            html.Div(
                className="card-group",
                children=[
                    html.Div(
                        className="card",
                        children=[
                            html.Div(
                                className="table-container",
                                id="table-container"
                            ),
                        ],
                    ),
                    html.Div(
                        className="card",
                        children=[
                            html.Div(
                                id="stats-table",
                                className="stats-table"
                            ),
                        ],
                    ),
                ],
            ),
                    html.Div(
                        className="other-pages",
                        children=[
                            html.Li(html.A("Analytics", href="/analytics"))
                        ]
                    )
                ],
                className="wrapper",
            ),
            html.Footer(
                id="footer",
                children=[
                    html.Div(
                        className="container",
                        children=[
                            html.Div(
                                className="copyright",
                                children=[
                                    html.Img(src="../static/img/CoE-Eng.png"),
                                    html.P(
                                        children=[
                                            html.Strong(
                                                children=[
                                                    html.Span(
                                                        "Prince of Songkla University"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            html.Div(
                                className="credits",
                                children=[
                                    html.A(
                                        "Artificial Intelligence Engineering"
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ]
    
    )

    @dash_app.callback(
        Output("air-quality-chart", "figure"),
        [Input("data", "value"), Input("parameter-filter", "value")],
    )
    def update_chart(data, parameter):
        df = pd.read_csv(f"website/data/{parameter}_predictions/{parameter}_{data}.csv")

        chart_figure = {
            "data": [
                {
                    "x": df["DATE"] + ' ' + df["TIME"],  
                    "y": df[parameter].values,
                    "type": "lines",
                },
            ],
            "layout": {
                "title": {"text": "PM25 Variation"},
                "xaxis": {"title": "Date Time"},
                "yaxis": {"title": "PM25"},
                "colorway": ["rgba(103, 176, 209, 0.8)"],
            },
        }
        return chart_figure


    @dash_app.callback(
        Output("stats-table", "children"),
        [
            Input("parameter-filter", "value"),
            Input("data", "value")
        ],
    )
    def update_stats_table(selected_parameter,data):
        df = pd.read_csv(f"website/data/{selected_parameter}_predictions/{selected_parameter}_{data}.csv")
        df["DATETIMEDATA"] = pd.to_datetime(df["DATE"] + ' ' + df["TIME"], format="%Y-%m-%d")

        filtered_data = df
        stats = filtered_data[selected_parameter].describe().reset_index().round(2)
        stats.columns = ["Statistic", "Value"]
        
        min_val = filtered_data[selected_parameter].min()
        min_date = filtered_data.loc[filtered_data[selected_parameter].idxmin()]["DATETIMEDATA"]
        max_val = filtered_data[selected_parameter].max()
        max_date = filtered_data.loc[filtered_data[selected_parameter].idxmax()]["DATETIMEDATA"]
        
        min_val_str = f"{min_val} ({min_date})"
        max_val_str = f"{max_val} ({max_date})"
        
        stats.loc[stats["Statistic"] == "min", "Value"] = min_val_str
        stats.loc[stats["Statistic"] == "max", "Value"] = max_val_str
        
        stats_table = dbc.Table.from_dataframe(stats, striped=True, bordered=True, hover=True, className="custom-table")
        
        title = html.Div(children=f"{selected_parameter} Statistics", className="custom-table",id='custom-table-head')
        
        return [title, stats_table]


    @dash_app.callback(
        Output('table-container', 'children'),
        [Input('data', 'value'), Input('parameter-filter', 'value')]
    )
    def display_table(data, parameter):
        df = pd.read_csv(f"website/data/{parameter}_predictions/{parameter}_{data}.csv")
        
        return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=12,
            style_cell={'textAlign': 'center'}
        )
    

    @dash_app.callback(
        Output("daily-stats", "figure"),
        [
            Input("parameter-filter", "value"),
            Input("data", "value")
        ],
    )
    def update_daily_stats(selected_parameter, data):
        df = pd.read_csv(f"website/data/{selected_parameter}_predictions/{selected_parameter}_{data}.csv")
        df["DATETIMEDATA"] = pd.to_datetime(df["DATE"] + ' ' + df["TIME"], format="%Y-%m-%d")
        filtered_data = df

        daily_stats = filtered_data.groupby(filtered_data["DATETIMEDATA"].dt.date)[selected_parameter].agg(['max', 'min', 'mean']).reset_index()

        traces = []
        for stat in ['max', 'min', 'mean']:
            traces.append(go.Scatter(
                x=daily_stats["DATETIMEDATA"],
                y=daily_stats[stat],
                mode='lines',
                name=stat.capitalize()  
            ))

        layout = {
            "title": f"{selected_parameter} Statistics",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": selected_parameter},
            "colorway": ["#8700f5","#62f5cb", "#1691f5" ],  
        }

        return {"data": traces, "layout": layout}

    
    return dash_app
