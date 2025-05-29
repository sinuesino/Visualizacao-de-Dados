import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Exploração de Dados", layout="wide")

tab1 = st.tabs(["📊 Visualização de Dados"])[0]

with tab1:
    st.header("Visualização de Dados")

    uploaded_file = st.file_uploader("Faça upload do arquivo CSV ou XLSX", type=["csv", "xlsx"], key="visual")

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, sep=None, engine="python")
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Tabela de dados")
        st.dataframe(df)

        colunas_disponiveis = df.columns.tolist()

        coluna_x = st.selectbox("Selecione a coluna para o eixo X", colunas_disponiveis, index=0)
        coluna_y = st.selectbox("Selecione a coluna para o eixo Y", colunas_disponiveis, index=1 if len(colunas_disponiveis) > 1 else 0)

        tipo_grafico = st.radio("Escolha o tipo de gráfico", ["Dispersão", "Linha", "Barras", "Histograma"])

        if coluna_x and coluna_y:
            if tipo_grafico == "Dispersão":
                fig = px.scatter(df, x=coluna_x, y=coluna_y)
            elif tipo_grafico == "Linha":
                df_agrupado = df.groupby(coluna_x, as_index=False)[coluna_y].mean().sort_values(by=coluna_x)
                fig = px.line(df_agrupado, x=coluna_x, y=coluna_y)
            elif tipo_grafico == "Barras":
                df_agrupado = df.groupby(coluna_x, as_index=False)[coluna_y].sum()
                fig = px.bar(df_agrupado, x=coluna_x, y=coluna_y)
            elif tipo_grafico == "Histograma":
                fig = px.histogram(df, x=coluna_x, y=coluna_y)

            st.plotly_chart(fig)
        else:
            st.warning("Selecione duas colunas para gerar o gráfico.")
    else:
        st.info("Por favor, envie um arquivo para visualizar.")
