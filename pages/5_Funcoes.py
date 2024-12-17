import streamlit as st
import pandas as pd
from time import sleep
from componentes import logout, tabelaPaginada

from model import salva_funcao, buscar_todas_funcoes
df = buscar_todas_funcoes()
def formFuncao():
    with st.form(key='form_funcao'):
        posicao = st.number_input(
            label="Posição",
            min_value=len(df) + 1,
            format="%d",
            help="Identificador único do colaborador."
        )

        descricao = st.text_input(
            label="Descrição",
            placeholder="Digite a descrição da Função",
            help="Descrição completa da função."
        )

        submit_button = st.form_submit_button(label="Salvar")
        cancel_button = st.form_submit_button(label="Cancelar")

    if submit_button:
            # Simulação de salvamento (substituir por lógica real)
            salva_funcao(posicao=posicao, descricao=descricao)
            st.success(f"Função '{descricao}' salva com sucesso!")
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
        usuario_logado = st.session_state['usuario']
        # Exibir a interface de pesquisa de funcoes
        with st.expander("Pesquisa de Funções", expanded=True):
            tabelaPaginada.show(df=df, n_linhas_iniciais=5)
        # Exibir o formulário de cadastro de funcoes
        with st.expander("Cadastro de Funções", expanded=False):
            formFuncao()
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()