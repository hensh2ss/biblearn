import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from biblearn.sword import loadData

import gensim

data = loadData('akjv')
st.title('Biblical Learning Toolkit (bibLearn) - Data Exploration Tool')
st.write("The following is a dashboard for interacting with basic statistics of the Bible.")
st.write("John 3:16:  {}".format(data))

#c. minson's model

model = gensim.models.Word2Vec.load("./MODELS/model.words.10")

KEYS = model.wv.index_to_key

CHOSEN = st.multiselect("Enter words below", KEYS)

send = st.button("Find similar words")

if send:
    result = model.wv.most_similar(positive=CHOSEN, topn=10)
    print(result)
    fig, ax = plt.subplots()
    x_val = [x[0] for x in result]
    y_val = [x[1] for x in result]
    ax.plot(x_val,y_val)
    plt.xticks(rotation = 45)
    st.pyplot(fig)
