import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


####### Graphing function #######
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.write_html('Revenue and Share Price', auto_open = True)

####### Using yfinance to extract share price data on Gamestop #######

GME = yf.Ticker('GME')
gme_data = GME.history(period = 'max')
gme_data.reset_index(inplace = True) # shows entry index 

######## Webscraping for Gamestop revenue data #######

url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html  = requests.get(url).text
html_data = BeautifulSoup(html, 'html.parser')

# locate gamestop revenue table 
gme_table = html_data.find_all("tbody")[1] 

# create empty dataframe for gamestop revenue data
gme_revenue = pd.DataFrame(columns = ['Date', 'Revenue']) 

# for loop to append date and revenue entries to gme_data datframe
for row in gme_table.find_all('tr'):
    col = row.find_all("td")
    Date = col[0].text
    Revenue = col[1].text
    gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

# Remove dollar signs and commas from revenue column   
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")    

# Removes null and empty strings in revenue column
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

make_graph(gme_data, gme_revenue, 'Gamestop')