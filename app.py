import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px

app = dash.Dash(__name__)

avocado = pd.read_csv('data_input/alpukat_fix.csv',sep=";", index_col=0)
avocado["Date"] = avocado['Date'].astype('Datetime64')
avocado.sort_values("Date", inplace=True)

avocado['SalesVolume'] = avocado['TypeA'] + avocado['TypeB'] + avocado['TypeC'] + avocado['TypeD'] +  avocado['TypeE'] + avocado['TypeG']

app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the Indonesia"
                    " between 2017 and 2020"
                    " "
                    " ",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Analysis', children = [
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(children="Region", className="menu-title"),
                                        dcc.Dropdown(
                                            id="region-filter",
                                            options=[
                                                {"label": City, "value": City}
                                                for City in np.sort(avocado.City.unique())
                                            ],
                                            value="Jakarta",
                                            clearable=False,
                                            className="dropdown",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Div(children="Type", className="menu-title"),
                                        dcc.Dropdown(
                                            id="type-filter",
                                            options=[
                                                {"label": avocado_type, "value": avocado_type}
                                                for avocado_type in avocado.Organic.unique()
                                            ],
                                            value="organic",
                                            clearable=False,
                                            searchable=False,
                                            className="dropdown",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        html.Div(
                                            children="Date Range",
                                            className="menu-title"
                                            ),
                                        dcc.DatePickerRange(
                                            id="date-range",
                                            min_date_allowed=avocado.Date.min().date(),
                                            max_date_allowed=avocado.Date.max().date(),
                                            start_date=avocado.Date.min().date(),
                                            end_date=avocado.Date.max().date(),
                                        ),
                                    ]
                                ),
                            ],
                            className="menu",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="price-chart",
                            ),
                            className="card",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="volume-chart",
                            ),
                            className="card",
                        ),
                        
                    ]),
                    dcc.Tab(label='Make your own analysis', children= [
                        html.H3('Make your own analysis')
                    ]),
                ]),
                html.Div(id='tabs-content')
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(City, avocado_type, start_date, end_date):
    data_filter = (
        (avocado.City == City)
        & (avocado.Organic == avocado_type)
        & (avocado.Date >= start_date)
        & (avocado.Date <= end_date)
    )
    filtered_data = avocado.loc[data_filter, :]

    avocado_groupdate = filtered_data.groupby('Date').mean().reset_index()

    price_chart_figure = px.line(avocado_groupdate,x="Date", y="AveragePrice")

    volume_chart_figure = px.scatter(filtered_data , 
                                        x = 'AveragePrice', 
                                        y='SalesVolume', 
                                        title="Perbandingan Harga Rata - Rata Alpukat Dengan Volume Penjualan",
                                        color='Year',
                                        marginal_x='histogram',
                                        marginal_y='violin',
                                        labels = {'SalesVolume' : 'Volume Penjualan',
                                                'AveragePrice' : 'Harga Rata - Rata'}
                        )
    
    return price_chart_figure, volume_chart_figure




if __name__ == "__main__":
    app.run_server(debug=True)