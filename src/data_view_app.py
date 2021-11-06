import streamlit as st
import pandas as pd
import numpy as np
from biblearn.sword import loadData

data = loadData('akjv')
st.title('Biblical Learning Toolkit (bibLearn) - Data Exploration Tool')
st.write("The following is a dashboard for interacting with basic statistics of the Bible.")
st.write("John 3:16:  {}".format(data))