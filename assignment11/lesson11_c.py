from dash import Dash, dcc, html, Input, Output  # Dash components you need
# Dash relies on Plotly to actually do the plotting.  Plotly creates an HTML page with lots of JavaScript.
import plotly.express as px
# This is only needed to give access to the Plotly built in datasets.
import plotly.data as pldata

df = pldata.stocks(return_type='pandas', indexed=False, datetimes=True)


# Initialize Dash app
# This creates the app object, to wich various things are added below.
app = Dash(__name__)
# __name__ is the name of the running Python module, which is your main module in this case

# Layout: This section creates the HTML components

app.layout = html.Div([  # This div is for the dropdown you see at the top, and also for the graph itself
    dcc.Dropdown(
        id="stock-dropdown",  # This creates the dropdown
        options=[{"label": symbol, "value": symbol} for symbol in df.columns], # This populates the dropdown with the list of stocks
        value="GOOG" # This is the initial value
    ),
    dcc.Graph(id="stock-price") # And the graph itself has to have an ID
])

# Callback for dynamic updates


@app.callback(  # OK, now this is a decorator.  Hmm, we haven't talked about decorators in Python.  This decorator is decorating the update_graph() function.
    # Because of the decorator, the update_graph() will be called when the stock-dropdown changes, passing the value selected in the dropdown.
    Output("stock-price", "figure"),  # And ... you get the graph back
    # When you pass in the value of the dropdown.
    [Input("stock-dropdown", "value")]
)
# This function is what actually does the plot, by calling Plotly, in this case a line chart of date (which is the index) vs. the chosen stock price.
def update_graph(symbol):
    fig = px.line(df, x="date", y=symbol, title=f"{symbol} Price")
    return fig


# Run the app
if __name__ == "__main__":  # if this is the main module of the program, and not something included by a different module
    app.run(debug=True)  # start the Flask web server
