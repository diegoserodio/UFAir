import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

"""
# Air pollution x COVID-19
"""

# Example map just for visualization purposes
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)

parameter1 = ['Air pollution', 'Land temperature', 'COVID-19 cases']
parameter2 = ['COVID-19 cases', 'Air pollution', 'Land temperature']

# Prevent choosing equal parameters to analyze, probably will be resolved with a better division for the params
def preventEqualParams(param1, param2):
    return 0

# First parameter:
add_selectbox1 = st.sidebar.selectbox(
    'Parameter #1',
    (parameter1)
)

# Second parameter:
add_selectbox2 = st.sidebar.selectbox(
    'Parameter #2',
    (parameter2)
)

# Visualization type:
add_selectbox = st.sidebar.selectbox(
    'Visualization type',
    ('Bubbles', 'Heat map', 'Graph')
)

preventEqualParams(add_selectbox1, add_selectbox2)
