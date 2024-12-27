import streamlit as st
import pandas as pd
from time import sleep
from componentes import logout, tabelaPaginada

from model import salva_treinamento, buscar_todos_treinamentos
df = buscar_todos_treinamentos()
def formTreinamento():
    with st.form(key='form_treinamento'):
        id = st.number_input(
            label="Codigo",
            min_value=1,
            value=len(df) + 1,
            format="%d",
            help="Identificador único do treinamento."
        )

        descricao = st.text_input(
            label="Descrição",
            placeholder="Digite a descrição do treinamento",
            help="Descrição completa do treinamento."
        )

        dias_valido = st.number_input(
            label="dias",
            min_value=1,
            format="%d",
            help="Validade do treinamento em dias."
        )

        tipo = st.text_input(
            label="Tipo",
            placeholder="Digite o tipo do treinamento",
            help="Descrição completa do tipo do treinamento."
        )

        submit_button = st.form_submit_button(label="Salvar")
        cancel_button = st.form_submit_button(label="Cancelar")

    if submit_button:
            # Simulação de salvamento (substituir por lógica real)
            salva_treinamento(id_treinamento=id, nome=descricao, dias_validade=dias_valido, tipo_treinamento=tipo)
            st.success(f"Treinamento '{descricao}' salvo com sucesso!")
            sleep(1)
            st.rerun()


    elif cancel_button:
        st.warning("Cadastro cancelado!")

# Função principal para gerenciar a interface de colaboradores
def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        st.warning("Você precisa estar logado para acessar esta página.")
        return
    else:
        st.set_page_config(page_title="CAPACITA-Treinamento", layout="wide", initial_sidebar_state="auto")
        usuario_logado = st.session_state['usuario']
        # Exibir a interface de pesquisa de funcoes
        with st.expander("Pesquisa de Treinamentos", expanded=True):
            tabelaPaginada.show(df=df, n_linhas_iniciais=5)
        # Exibir o formulário de cadastro de funcoes
        with st.expander("Cadastro de Treinamento", expanded=False):
            formTreinamento()
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()
