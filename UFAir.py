import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly as py
import plotly.express as px
import sweetviz as sv
import codecs
import seaborn as sns
import reverse_geocode

covid = pd.read_csv("./Data/WHO-COVID-19-global-data.csv")
covid = covid.rename(columns={' Country':'Country', ' Cumulative_cases':'Cumulative_cases'})
covid_countries = covid.groupby(['Country','Date_reported']).sum().reset_index().sort_values('Date_reported', ascending=True)
covid_countries = covid_countries[covid_countries['Cumulative_cases']>0]
worldmap = px.choropleth(covid_countries,
                     locations='Country',
                     locationmode='country names',
                     color='Cumulative_cases',
                     hover_name='Country',
                     animation_frame='Date_reported'
                 )
worldmap.update_layout(title_text='',
                 title_x=0.5,
                 geo=dict(
                     showcoastlines=True,)
                 )


df_pollution=pd.read_csv('./Data/df_pollution.csv')

# Let's create a column in the dataframe that is the lat, long convert to the country name
@st.cache
def getCountryFromCoord():
    latlon_country = []
    for i in range(0, len(df_pollution)):
        coordinates = (df_pollution['lat'][i], df_pollution['long'][i]),
        latlon_country.append(reverse_geocode.search(coordinates)[0]['country'])
    loading = False
    return latlon_country

df_pollution['Country'] = getCountryFromCoord()

# Let's group the dataset by country, day and then sum the values from each day
df_pollution = df_pollution.groupby(['Country','date']).sum().reset_index().sort_values('date', ascending=True)

# Let's plot the mapa mundi chart for a date greater than 2020-01-01 and the CO2 emission

df_pollution_new = df_pollution[df_pollution['date']>='2020-01-04']

map_pollution = px.scatter_geo(df_pollution_new,
                     locations='Country',
                     locationmode='country names',
                     color='Alt_Mean_co2',
                     hover_name='Country',
                     animation_frame='date',
                     size='Alt_Mean_co2'
                 )
map_pollution.update_layout(title_text='',
                 title_x=0.5,
                 geo=dict(
                     showcoastlines=True,)
                 )

# Let's merge the covid and the pollution dataframe
@st.cache
def mergeDataframes(a, b, header):
    return pd.merge(a, b, on=header)

pollution_and_covid = mergeDataframes(covid_countries, df_pollution_new, 'Country')

# Let's create the correlation between the columns
corr_matrix= pollution_and_covid.corr()[[' New_cases','Cumulative_cases',' New_deaths',' Cumulative_deaths',
                           'Alt_Mean_co2','Alt_Mean_no2','Alt_Mean_ch4','Alt_Mean_o3']]

corr_matrix.drop(['lat', 'long'], inplace=True)
# This will maks the values mirrored
mask = np.zeros_like(corr_matrix, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Plot the correlation matrix chart
f, ax = plt.subplots(figsize=(11, 15))
heatmap = sns.heatmap(corr_matrix,
                      mask = mask,
                      square = True,
                      linewidths = .5,
                      cmap = 'coolwarm',
                      cbar_kws = {'shrink': .4,
                                'ticks' : [-1, -.5, 0, 0.5, 1]},
                      vmin = -1,
                      vmax = 1,
                      annot = True,
                      annot_kws = {'size': 12})
#add the column names as labels
sns.set_style({'xtick.bottom': True}, {'ytick.left': True})

# First parameter:
param1 = st.sidebar.selectbox(
    'Parameter #1',
    (['Air pollution'])
)

# Second parameter:
param2 = st.sidebar.selectbox(
    'Parameter #2',
    (['COVID-19 cases'])
)

# Visualization type:
vType = st.sidebar.selectbox(
    'Visualization type',
    ('Heat map', 'Bubbles', 'Correlation Matrix')
)

# def st_display_sweetviz(report_html,width=1000,height=500):
# 	report_file = codecs.open(report_html,'r')
# 	page = report_file.read()
# 	components.html(page,width=width,height=height,scrolling=True)

def setVisualization(type):
    if type=='Heat map':
        st.write(worldmap)
    elif type=='Bubbles':
        st.write(map_pollution)
    elif type=='Correlation Matrix':
        st.write(corr_matrix)

st.write("#",param1, " x ",  param2)

# if param1=='Air pollution':
#     defaultcols = ["Cumulative_cases","Date_reported"]
#     cols = st.multiselect("Attributes", covid.columns.tolist(), default=defaultcols)
#     st.dataframe(covid[cols].head(10))
#
#
# if param1=='COVID-19 cases':
# 	st.dataframe(covid.head())
# 	if st.button("Generate Sweetviz Report"):
# 		# Normal Workflow
# 		report = sv.analyze(covid)
# 		report.show_html()
# 		st_display_sweetviz("SWEETVIZ_REPORT.html")

st.write("###", vType)

setVisualization(vType)
#st.write(fig)
