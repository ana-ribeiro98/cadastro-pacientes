import os
from datetime import datetime

import gradio as gr
import pandas as pd

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]


def ler_ultimos(n=5):
    # Se o arquivo ainda não existe, devolve uma tabela vazia só com os títulos
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)
    return pd.read_csv(ARQUIVO_CSV).tail(n)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome or not nome.strip():
        return "⚠️ Informe o nome do paciente.", ler_ultimos()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": idade,
        "convenio": convenio,
        "prioridade": prioridade,
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    return "✅ Paciente cadastrado com sucesso!", ler_ultimos()


with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")

    nome = gr.Textbox(label="Nome do paciente")

    idade = gr.Number(label="Idade", precision=0)

    convenio = gr.Dropdown(
        choices=["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
        value="Particular",
        filterable=False,
        interactive=True,
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        value=3,
        step=1,
        label="Prioridade do atendimento (5 = urgente)",
        interactive=True,
    )

    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)

    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", interactive=False)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

    # Ao abrir a página, já mostra os cadastros que existirem no arquivo
    demo.load(ler_ultimos, None, tabela)

demo.launch()