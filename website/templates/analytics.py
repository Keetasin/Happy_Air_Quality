import dash
from dash import dcc, html, dash_table
import dash_table
import pandas as pd
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

df1 = pd.read_csv("website/data/after_clean/cleaned_Songkhla.csv")
df2 = pd.read_csv("website/data/after_clean/cleaned_Mueang_Yala.csv")
df3 = pd.read_csv("website/data/after_clean/cleaned_Betong_Yala.csv")
df4 = pd.read_csv("website/data/after_clean/cleaned_Nakhon_Si_Thammarat.csv")
df5 = pd.read_csv("website/data/after_clean/cleaned_Narathiwat.csv")
df6 = pd.read_csv("website/data/after_clean/cleaned_Phuket.csv")
df7 = pd.read_csv("website/data/after_clean/cleaned_Satun.csv")
df8 = pd.read_csv("website/data/after_clean/cleaned_Surat_Thani.csv")
df9 = pd.read_csv("website/data/after_clean/cleaned_Trang.csv")

df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9]

for df in df_list:
    df["DATETIMEDATA"] = pd.to_datetime(df["DATE"] + ' ' + df["TIME"], format="%Y-%m-%d")
    df.sort_values("DATETIMEDATA", inplace=True)

external_stylesheets = [
    {
        "href": "/static/css/style2.css",
        "rel": "stylesheet",
    },
]

def create_analytics_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", external_stylesheets=external_stylesheets, url_base_pathname="/analytics/")
    dash_app.title = "Happy Air Quality Analytics"
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
                                                    html.Li("Analytics")
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
                        children="Happy Air Quality Analytics", className="header-title"
                    ),
                    html.P(
                        children="Analyze the air quality data from air4thai",
                        className="header-description",
                    ),
                    html.P(
                        children="Since 01/01/2023 - Current",
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
                                    {"label": "Songkhla", "value": "df1"},
                                    {"label": "Mueang,Yala", "value": "df2"},
                                    {"label": "Betong,Yala", "value": "df3"},
                                    {"label": "Nakhon Si Thammarat", "value": "df4"},
                                    {"label": "Narathiwat", "value": "df5"},
                                    {"label": "Phuket", "value": "df6"},
                                    {"label": "Satun", "value": "df7"},
                                    {"label": "Surat Thani", "value": "df8"},
                                    {"label": "Trang", "value": "df9"},
                                ],
                                value="df1",
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
                                    {"label": parameter, "value": parameter}
                                    for parameter in df1.columns[2:-1]
                                ],
                                value="PM25",
                                clearable=False,
                                className="dropdown-parameter",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children="Date Range",
                                className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=df1["DATETIMEDATA"].min().date(),
                                max_date_allowed=df1["DATETIMEDATA"].max().date(),
                                start_date=df1["DATETIMEDATA"].min().date(),
                                end_date=df1["DATETIMEDATA"].max().date(),
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
                            html.Li(html.A("Predictions", href="/prediction"))
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
        [Input("data", "value"), Input("parameter-filter", "value"), Input("date-range", "start_date"), Input("date-range", "end_date")],
    )
    def update_chart(data, parameter, start_date, end_date):
        df_index = int(data.split("df")[1]) - 1
        df = df_list[df_index]

        filtered_data = df[(df["DATETIMEDATA"] >= start_date) & (df["DATETIMEDATA"] <= end_date)]
        chart_figure = {
            "data": [
                {
                    "x": filtered_data["DATETIMEDATA"],
                    "y": filtered_data[parameter],
                    "type": "lines",
                },
            ],
            "layout": {
                "title": {"text": f"{parameter} Variation"},
                "xaxis": {"title": "Date Time"},
                "yaxis": {"title": parameter},
                "colorway": ["rgba(103, 176, 209, 0.8)"],
            },
        }
        return chart_figure


    @dash_app.callback(
        Output("stats-table", "children"),
        [
            Input("parameter-filter", "value"),
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
        ],
    )
    def update_stats_table(selected_parameter, start_date, end_date):
        mask = (
            (df["DATETIMEDATA"] >= start_date)
            & (df["DATETIMEDATA"] <= end_date)
        )
        filtered_data = df.loc[mask]
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
        [Input('data', 'value'), Input('date-range', 'start_date'), Input('date-range', 'end_date'), Input('parameter-filter', 'value')]
    )
    def display_table(data, start_date, end_date, parameter):
        df_index = int(data.split("df")[1]) - 1
        df = df_list[df_index]
        filtered_df = df[(df["DATETIMEDATA"] >= start_date) & (df["DATETIMEDATA"] <= end_date)]
        columns_to_display = ["DATE", "TIME", parameter]
        return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in columns_to_display],
            data=filtered_df[columns_to_display].to_dict('records'),
            page_size=12,  
            style_cell={'textAlign': 'center'}  
        )
    
    @dash_app.callback(
        Output("daily-stats", "figure"),
        [
            Input("parameter-filter", "value"),
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
        ],
    )
    def update_daily_stats(selected_parameter, start_date, end_date):
        mask = (
            (df["DATETIMEDATA"] >= start_date)
            & (df["DATETIMEDATA"] <= end_date)
        )
        filtered_data = df.loc[mask]

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
