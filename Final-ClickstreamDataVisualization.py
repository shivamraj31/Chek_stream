"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

import codecs

# Components Pkgs
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report

# Custome Component Fxn
import sweetviz as sv 


#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#from dash.dependencies import Input, Output

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)


def pieChart(numArray,labs):
    x = np.array(numArray)
    mylabels = labs

    fig = plt.figure(figsize=(10, 4))
    plt.pie(x, labels = mylabels)

    st.balloons()
    st.pyplot(fig)
file_path= r"C:\Users\gprak\OneDrive\Desktop\NetworthCorp\Customer Raw data.xlsx"
df = pd.read_excel(file_path,engine='openpyxl')

if st.button("Generate Sweetviz Report"):
    # Normal Workflow
    report = sv.analyze(df)
    report.show_html()
    st_display_sweetviz("SWEETVIZ_REPORT.html")

df



st.write("1) Hits - Number of Search Queries")

a = df['Product Name'].value_counts()
a


df1=df.select_dtypes(exclude=['int32','int64','float32','float64'])
selected_columns = st.multiselect("select any column from dataset", df1.columns, default="PID")
s = df[selected_columns[0]].str.strip().value_counts()
trace = go.Bar(x=s.index,y=s.values,showlegend = False)
layout = go.Layout(title = "Choose multiple columns :- ")
data = [trace]
fig = go.Figure(data=data,layout=layout)
st.plotly_chart(fig)

st.write("2) Click-throughs - Number of times visitors clicked on any one of the results in the search listing page")

b = df['PID'].value_counts()
#b
selected_columns = st.multiselect("select any PID from dataset", ['Category'], default="Category")
s = df[selected_columns[0]].str.strip().value_counts()
trace = go.Bar(x=s.index,y=s.values,showlegend = False)
layout = go.Layout(title = "Choosen category columns :- ")
data = [trace]
fig = go.Figure(data=data,layout=layout)
st.plotly_chart(fig)

st.write("3) Clicks - Cumulative Number of times visitors clicked on any result in the search listing page")
#c=df.describe()
#c

#df=df.rename(columns={'PID':'value'})
names=list(df1.columns)
numArrays=[]
labs=[]
for x in list(df1.columns):
    #df['x']=df[x]
    df['value']=df[x]
    # Frequency
    stats_df = df \
    .groupby('value') \
    ['value'] \
    .agg('count') \
    .pipe(pd.DataFrame) \
    .rename(columns = {'value': 'frequency'})

    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    stats_df

    # Plot the discrete Probability Mass Function and CDF.
    # Technically, the 'pdf label in the legend and the table the should be 'pmf'
    # (Probability Mass Function) since the distribution is discrete.
    numArrays.append(stats_df['pdf'])
    labs.append(stats_df['value'])
    # If you don't have too many values / usually discrete case
    if x in ['Category','Fabric']:
        #numArray = stats_df['pdf']
        #labs = stats_df['value']
        st.set_option('deprecation.showPyplotGlobalUse', False)
        stats_df.plot.bar(x = 'value', y = ['pdf', 'cdf'], grid = True)
        st.pyplot()

st.write("4) CTR = Clickthrough rate = Click Throughs/Hits")

for x in list(df1.columns):
    a=df1[x].value_counts()/len(df1)
    st.write(x)
    st.write(a)

st.write("5) Orders - Orders placed against the search query (Query report) or for the particular product (Product Performance report)")



#pieChart(numArray,labs)
option = st.selectbox(
     'How would you like to be contacted?',
     tuple(names))

st.write('You selected:', option)
#st.write(names.index(option))

numArray = numArrays[names.index(option)]
#st.write(numArray)

lab  = labs[names.index(option)]
pieChart(numArray,lab)
