import streamlit as st
import pandas as pd
from componentes import logout, tabelaPaginada

from model import salva_processo, buscar_todos_procesos

df = buscar_todos_procesos()
def formProcesso():
    with st.form(key='form_processo'):
        cdc = st.number_input(
            label="Centro de Custo",
            min_value=len(df) + 1,
            format="%d",
            help="Identificador único do centro de custo."
        )

        descricao = st.text_input(
            label="Descrição",
            placeholder="Digite a descrição do centro de custo",
            help="Descrição completa do centro de custo."
        )

        processo = st.text_input(
            label="Processo",
            placeholder="Digite a descrição do processo",
            help="Descrição completa do processo."
        )

        submit_button = st.form_submit_button(label="Salvar")
        cancel_button = st.form_submit_button(label="Cancelar")

    if submit_button:
            # Simulação de salvamento (substituir por lógica real)
            salva_processo(cdc=cdc, descricao=descricao, processo=processo)
            st.success(f"Centro de Custo '{descricao}' salvo com sucesso!")
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
        usuario_logado = st.session_state['usuario']
        # Exibir a interface de pesquisa de funcoes
        with st.expander("Pesquisa de Processo", expanded=True):
            tabelaPaginada.show(df=df, n_linhas_iniciais=5)
        # Exibir o formulário de cadastro de funcoes
        with st.expander("Cadastro de Centro de Custo", expanded=False):
            formProcesso()
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()