# Main Dash app to create the real time dashboard
from dash import Dash, dcc, html, Input, Output #type: ignore
import plotly.graph_objs as go #type: ignore
from data_fetcher import fetch_stock_data

app = Dash(__name__) #initialize the dash app instance
server = app.server

symbol = "AAPL"

app.layout = html.Div([
    html.H1(f"Real Time Stock Dashboard", style={"textAlign": "center"}),
    html.Div([ #inner div contains the dropdown
        html.Label("Select Stock Symbol:"),
        dcc.Dropdown(
            id = "stock-symbol-dropdown",
            options=[
                {"label":"Apple", "value":"AAPL"},
                {"label":"Microsoft", "value":"MSFT"},
                {"label":"Google", "value":"GOOGL"},
                {"label":"Amazon", "value":"AMZN"}
            ],
            value="AAPL",
            clearable=False
        )
    ], style= {"width": "50%", "margin": "auto"}),
    dcc.Graph(id="stock-price-chart"), #graph to display the stock price
    dcc.Interval( #creates an interval component that triggers callbacks at a specific interval
        id="interval-component",
        interval=60*1000, # in milliseconds for 1 minute
        n_intervals=0 #triggers callback by incrementing this value at the specified interval
    )
])

#callback to update the stock price chart
@app.callback(
    Output("stock-price-chart", "figure"), #update the figure property of the graph
    [Input("interval-component", "n_intervals"), #listed as input to trigger the callback, each time n_intervals changes, update_stock_chart function is called
     Input("stock-symbol-dropdown", "value")]
)
def update_stock_chart(n_intervals, selected_symbol):
    stock_data = fetch_stock_data(selected_symbol) 
    if stock_data.empty:
        return {
            "data": [],
            "layout": {
                "title": f"No data available for {selected_symbol}",
                "xaxis": {"title" : "Time"},
                "yaxis": {"title" : "Price(USD)"}
            }
        }
    figure = {
        "data" : [
            go.Scatter(
                x = stock_data.index,
                y = stock_data["Close"].astype(float),
                mode = "lines",
                name = "Close Price"
            )
        ], 
        "layout" : {
            "title": f"Stock Prices for {selected_symbol} (Close)",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Price (USD)"}
        }   
    }
    return figure
if __name__ == "__main__":
    app.run_server(debug = True)
