#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[2]:


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
    fig.show()


# # Question 1

# NOTE: None of the installs listed in this notebook would install properly in JupyterLab or IBM Watson due to dependency issues that I couldn't figure out easily. It was significantly faster to recreate this notebook locally, therefore the markdown will be organized differently from the Coursera NB provided.

# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.
# 
# Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to max so we get information for the maximum amount of time.
# 
# **Reset the index** using the `reset_index(inplace=True)` function on the tesla_data DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.

# In[3]:


Tesla = yf.Ticker("TSLA")


# In[4]:


tesla_data = Tesla.history(period="max")


# In[5]:


tesla_data.reset_index(inplace=True)


# In[6]:


tesla_data.head()


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named `html_data`.

# In[7]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url)
html_data.status_code


# Parse the html data using beautiful_soup.

# In[8]:


soup = BeautifulSoup(html_data.text, "html5lib")


# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Quarterly Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.

# In[9]:


table = pd.read_html(url, match = 'Tesla Quarterly Revenue')
tesla_revenue_wrongnames = table[0]
tesla_revenue = tesla_revenue_wrongnames.rename(columns={"Tesla Quarterly Revenue (Millions of US $)":"Date", "Tesla Quarterly Revenue (Millions of US $).1":"Revenue"})
tesla_revenue.head()


# Execute the following line to remove the comma and dollar sign from the `Revenue` column. 

# In[10]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"", regex=True)


# Execute the following lines to remove an null or empty strings in the Revenue column.

# In[11]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.

# In[12]:


tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract Stock Data

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.

# In[13]:


GME = yf.Ticker("GME")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.

# In[14]:


gme_data = GME.history(period = "max")


# **Reset the index** using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.

# In[15]:


gme_data.reset_index(inplace=True)
gme_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data`.

# In[16]:


html_data = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html")


# Parse the html data using `beautiful_soup`.

# In[17]:


data = BeautifulSoup(html_data.text,"html5lib")


# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Quarterly Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`. Make sure the comma and dollar sign is removed from the `Revenue` column using a method similar to what you did in Question 2.
# 

# In[18]:


table = pd.read_html("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html", match = 'GameStop Quarterly Revenue')
df = table[0]
gme_revenue = df.rename(columns={"GameStop Quarterly Revenue (Millions of US $)":"Date", "GameStop Quarterly Revenue (Millions of US $).1":"Revenue"})
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"", regex=True)
gme_revenue.head()


# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.

# In[19]:


gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph

# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`. Note the graph will only show data upto June 2021.
# 

# In[20]:


make_graph(tesla_data, tesla_revenue, 'Tesla Historical Stock and Revenue')


# ## Question 6: Plot GameStop Stock Graph

# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.

# In[21]:


make_graph(gme_data, gme_revenue, 'GameStop Historical Stock and Revenue')


# In[ ]:




