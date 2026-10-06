import streamlit as st
import pandas as pd
from datetime import datetime

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("Cadastro de Pacientes")

# Memória da sessão: guarda os pacientes cadastrados enquanto o app está aberto
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("cadastro", clear_on_submit=False):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5, 3)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar")

if enviado:
    if not nome.strip():
        st.warning("Informe o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo,
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha], columns=COLUNAS)],
            ignore_index=True,
        )
        st.success("Paciente cadastrado com sucesso!")

st.subheader("Últimos pacientes cadastrados")
st.dataframe(st.session_state.pacientes.tail(5), use_container_width=True)

csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Baixar CSV",
    data=csv,
    file_name="pacientes.csv",
    mime="text/csv",
)
