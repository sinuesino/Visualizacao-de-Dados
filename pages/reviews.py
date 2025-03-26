MODO_DEBUG = False

import streamlit as st

if not MODO_DEBUG:
    st.stop()
st.title("Página de Reviews 📊")
st.write("Aqui estão os reviews...")

import streamlit as st
import pandas as pd

df_reviews = pd.read_csv("datasets/customer reviews.csv")
df_top100_books = pd.read_csv("datasets/Top-100 Trending Books.csv")

livros = df_top100_books["book title"].unique()
livro = st.sidebar.selectbox("Books", livros)

df_livro = df_top100_books[df_top100_books["book title"] == livro]
df_reviews_filtro = df_reviews[df_reviews["book name"] == livro]

titulo_livro = df_livro["book title"].iloc[0]
genero_livro = df_livro["genre"].iloc[0]
preco_livro = df_livro["book price"].iloc[0]
nota_livro = df_livro["rating"].iloc[0]
ano_livro = df_livro["year of publication"].iloc[0]

st.title(titulo_livro)
st.subheader(genero_livro)
col1, col2, col3 = st.columns(3)
col1.metric("Preço", preco_livro)
col2.metric("Notas do livro", nota_livro)
col3.metric("Ano de publicação", ano_livro)

st.divider()

for row in df_reviews_filtro.values:
    mensagem = st.chat_message(f"{row[4]}")
    mensagem.write(f"**{row[2]}**")
    mensagem.write(row[5])
