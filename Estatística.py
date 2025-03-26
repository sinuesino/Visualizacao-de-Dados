import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Escolha um arquivo CSV ou XLSX", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
    else:
        df = pd.read_excel(uploaded_file)

    st.write("📊 Visualização dos dados:")
    st.dataframe(df)

    colunas_disponiveis = df.columns.tolist()

    coluna_x = st.selectbox("Selecione a coluna para o eixo X", colunas_disponiveis, index=0)
    coluna_y = st.selectbox("Selecione a coluna para o eixo Y", colunas_disponiveis, index=1 if len(colunas_disponiveis) > 1 else 0)

    tipo_grafico = st.radio(
        "Escolha o tipo de gráfico",
        ["Dispersão", "Linha", "Barras", "Histograma"]
    )

    if coluna_x and coluna_y:
        if tipo_grafico == "Dispersão":
            fig = px.scatter(df, x=coluna_x, y=coluna_y, title=f"Gráfico de Dispersão: {coluna_x} vs {coluna_y}")
        elif tipo_grafico == "Linha":
            fig = px.line(df, x=coluna_x, y=coluna_y, title=f"Gráfico de Linha: {coluna_x} vs {coluna_y}")
        elif tipo_grafico == "Barras":
            fig = px.bar(df, x=coluna_x, y=coluna_y, title=f"Gráfico de Barras: {coluna_x} vs {coluna_y}")
        elif tipo_grafico == "Histograma":
            fig = px.histogram(df, x=coluna_x, y=coluna_y, title=f"Histograma: {coluna_x} vs {coluna_y}")

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ Selecione duas colunas para gerar o gráfico.")
else:
    st.info("📂 Por favor, faça o upload de um arquivo CSV ou XLSX.")
