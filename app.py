import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time

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
    ('Bubbles', 'Heat map', 'Graph')
)

preventEqualParams(param1, param2)

st.write("#",param1, " x ",  param2)
st.write("###", vType)

# Example map just for visualization purposes
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)
