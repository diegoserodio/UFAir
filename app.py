import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly as py
import plotly.express as px
import sweetviz as sv
import codecs

covid = pd.read_csv("./Data/WHO-COVID-19-global-data.csv")
covid = covid.rename(columns={' Country':'Country', ' Cumulative_cases':'Cumulative_cases'})
covid_countries = covid.groupby(['Country','Date_reported']).sum().reset_index().sort_values('Date_reported', ascending=True)
covid_countries = covid_countries[covid_countries['Cumulative_cases']>0]
fig = px.choropleth(covid_countries,
                     locations='Country',
                     locationmode='country names',
                     color='Cumulative_cases',
                     hover_name='Country',
                     animation_frame='Date_reported'
                 )
fig.update_layout(title_text='World Coronavírus Spread',
                 title_x=0.5,
                 geo=dict(
                     showcoastlines=True,)
                 )

parameters1 = ['Air pollution', 'Land temperature', 'COVID-19 cases']
parameters2 = ['COVID-19 cases', 'Air pollution', 'Land temperature']

# Prevent choosing equal parameters to analyze, probably will be resolved with a better division for the params
def preventEqualParams(param1, param2):
    return 0

# First parameter:
param1 = st.sidebar.selectbox(
    'Parameter #1',
    (parameters1)
)

# Second parameter:
param2 = st.sidebar.selectbox(
    'Parameter #2',
    (parameters2)
)

# Visualization type:
vType = st.sidebar.selectbox(
    'Visualization type',
    ('Heat map', 'Bubbles', 'Graph')
)

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)

preventEqualParams(param1, param2)

st.write("#",param1, " x ",  param2)

if param1=='Air pollution':
    defaultcols = ["Cumulative_cases","Date_reported"]
    cols = st.multiselect("Attributes", covid.columns.tolist(), default=defaultcols)
    st.dataframe(covid[cols].head(10))


if param1=='COVID-19 cases':
	st.dataframe(covid.head())
	if st.button("Generate Sweetviz Report"):
		# Normal Workflow
		report = sv.analyze(covid)
		report.show_html()
		st_display_sweetviz("SWEETVIZ_REPORT.html")

st.write("###", vType)

st.write(fig)
