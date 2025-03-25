import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df_reviews = pd.read_csv("datasets/customer reviews.csv")
df_top100_books = pd.read_csv("datasets/Top-100 Trending Books.csv")

preco_maximo = df_top100_books["book price"].max()
preco_minimo = df_top100_books["book price"].min()

valores = st.sidebar.slider("qual a faixa de preço?", preco_minimo, preco_maximo, preco_maximo)
df_livros = df_top100_books[df_top100_books["book price"] <= valores]
df_livros

grafico = px.bar(df_livros["year of publication"].value_counts())
grafico2 = px.histogram(df_livros["book price"])

col1, col2 = st.columns(2)
col1.plotly_chart(grafico)
col2.plotly_chart(grafico2)
