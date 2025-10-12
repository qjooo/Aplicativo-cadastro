import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard - Clínica de Estética", layout="wide")

st.title("Consultas H.P. Estética")

arquivo = "consultas.csv"

if os.path.exists(arquivo):
    colunas = ["Nome", "E-mail", "Data", "Tratamento", "Pagamento"]
    df = pd.read_csv(arquivo, names=colunas, header=None)

    # Criar coluna auxiliar para o nome principal do tratamento
    df["Tratamento Principal"] = df["Tratamento"].str.extract(r'^([^(]+)').iloc[:,0].str.strip()
    # Criar coluna auxiliar para o nome principal do pagamento
    df["Pagamento Principal"] = df["Pagamento"].str.extract(r'^([^(]+)').iloc[:,0].str.strip()

    st.sidebar.header("Filtros")
    tratamentos = st.sidebar.multiselect(
        "Filtrar por Tratamento:",
        df["Tratamento Principal"].unique()
    )
    pagamentos = st.sidebar.multiselect(
        "Filtrar por Pagamento:",
        df["Pagamento Principal"].unique()
    )

    if tratamentos:
        df = df[df["Tratamento Principal"].isin(tratamentos)]
    if pagamentos:
        df = df[df["Pagamento Principal"].isin(pagamentos)]

    # tabela principal (mostra tratamento e pagamento completos)
    st.subheader("Lista de Consultas")
    st.dataframe(df[["Nome", "E-mail", "Data", "Tratamento", "Pagamento"]], use_container_width=True)

    # estatísticas
    st.subheader("Estatísticas Totais")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de Consultas", len(df))
        st.metric("Pacientes Únicos", df["Nome"].nunique())
        st.metric("Pacientes que Retornaram", df["Nome"].value_counts().loc[lambda x: x > 1].count())
        st.metric("Formas de Pagamento", df["Pagamento Principal"].nunique())

    with col2:
        # Gráfico de barras dos tratamentos
        counts = df["Tratamento Principal"].value_counts()
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            color=counts.index,
            color_discrete_map={
                "Limpeza de Pele": "#1f77b4",
                "Harmonização Facial": "#ff7f0e",
                "Rinomodelação": "#2ca02c",
                "Peeling": "#d62728"
            },
            color_discrete_sequence=None,
            labels={"x": "Tratamento", "y": "Quantidade"},
            title="Consultas por Tratamento"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico de pizza para os métodos de pagamentos (usando apenas o principal)
        counts_pagamento = df["Pagamento Principal"].value_counts()
        fig2 = px.pie(
            names=counts_pagamento.index,
            values=counts_pagamento.values,
            color=counts_pagamento.index,
            color_discrete_map={
                "Pix": "#00b894",
                "Dinheiro": "#fdcb6e",
                "Cartão Débito": "#0984e3",
                "Cartão Crédito": "#6c5ce7",
                "Boleto": "#ff00ea"
            },
            color_discrete_sequence=None,
            title="Consultas por Meio de Pagamento"
        )
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Nenhum cadastro encontrado. O arquivo 'consultas.csv' ainda não existe.")