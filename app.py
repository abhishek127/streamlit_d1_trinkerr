import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

DATA_URL = (
    "raw.csv"
)

st.title("D1 Ratio Analysis for customer retention")
st.sidebar.title("D1 Ratio Analysis for customer retention")
st.markdown("This application is a Streamlit dashboard used "
            "to analyze D1 Ratio for customer retention")
st.sidebar.markdown("This application is a Streamlit dashboard used "
            "to analyze D1 Ratio for customer retention")

def get_d1(x):
    a=x["username_list"]
    b=x["next_day_user"]
    try:
        d1_users=np.intersect1d(a,b)
        return(len(d1_users)/len(a))
    except:
        return(np.nan)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data.signup_date = pd.to_datetime(data.signup_date, format='%d/%m/%Y')
    data.ref_date = pd.to_datetime(data.ref_date, format='%d/%m/%Y')
    df["signup_date"]=df['signup_date'].dt.date
    df["ref_date"]=df['ref_date'].dt.date
    return data

data = load_data()
#show data
st.sidebar.subheader("See your data:")
if st.sidebar.checkbox("Show Dataset"):
    head=st.sidebar.radio("View from top(Head) or bottom(Tail)",("Head","Tail"))
    if head=="Head":
        st.dataframe(data.head(10))
    else:
        st.dataframe(data.tail(10))

st.sidebar.subheader("Check D1 ratio:")
if st.sidebar.checkbox("Show D1"):
    select=st.sidebar.selectbox("Visulaisation type",["Bar Plot", "Line Plot"])
    df=data[["username","ref_date"]]
    group = df.groupby('ref_date')
    df2 = group.apply(lambda x: x['username'].unique())
    df2=df2.reset_index()
    df2.columns=["ref_date","username_list"]
    df2["next_day_user"]=df2["username_list"].shift(-1)
    df2["D1_ratio"]=df2.apply(lambda x: get_d1(x),axis=1)
    df2.dropna()
    if select=="Bar Plot":
        fig = px.bar(df2, x='ref_date', y='D1_ratio', color='D1_ratio', height=500)
        st.plotly_chart(fig)
    elif select=="Line Plot":
        fig = go.Figure(data=go.Scatter(x=df2["ref_date"],y=df2["D1_ratio"]))
        st.plotly_chart(fig)

st.sidebar.header("Word Cloud for most frequent user")
if st.sidebar.checkbox("Show Wordcloud"):
    df = data[["username"]]
    words = ' '.join(df['username'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

