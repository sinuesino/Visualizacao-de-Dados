import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain_experimental.agents import create_csv_agent
import os
from transformers import pipeline

st.set_page_config(page_title="Exploração e Perguntas com IA", layout="wide")

load_dotenv()

if "HUGGINGFACE_API_KEY" not in os.environ:
    st.warning("Token da HuggingFace não encontrado no ambiente. Verifique seu arquivo .env")

pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

tab1, tab2 = st.tabs(["📊 Visualização de Dados", "🤖 Pergunte com IA"])

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
'''

DESENVOLVENDO A PARTE DE IA

with tab2:
    st.header("Faça perguntas sobre seu arquivo com IA")

    user_csv = st.file_uploader("Envie um arquivo CSV ou XLSX para análise por IA", type=["csv", "xlsx"], key="qa")

    if user_csv is not None:
        user_question = st.text_input("O que você quer saber sobre os dados?")

        if user_question:
            with st.spinner("Analisando..."):
                try:
                    # Carrega os dados
                    if user_csv.name.endswith('.csv'):
                        df = pd.read_csv(user_csv)
                    else:
                        df = pd.read_excel(user_csv)
                    
                    # Configura o LLM CORRETAMENTE
                    from transformers import T5ForConditionalGeneration, T5Tokenizer
                    
                    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
                    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
                    
                    # Pré-processa a pergunta
                    input_text = f"question: {user_question} context: {df.to_string()}"
                    input_ids = tokenizer.encode(input_text, return_tensors="pt")
                    
                    # Gera a resposta
                    outputs = model.generate(input_ids)
                    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    
                    st.success("Resposta:")
                    st.write(resposta)
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
                    st.info("Dica: Verifique se você tem os pacotes transformers e torch instalados")
    else:
        st.info("Envie um arquivo para poder perguntar.")
'''