import streamlit as st
import pandas as pd
from componentes import logout, tabelaPaginada

from model import buscar_todos_usuarios, salva_usuario

df = buscar_todos_usuarios()
def formUsuario():
    with st.form(key='form_usuario'):
        id = st.number_input(
            label="Codigo",
            min_value=1,
            value=len(df) + 1,
            format="%d",
            help="Identificador único do usuario."
        )

        nome = st.text_input(
            label="Nome",
            placeholder="Digite o nome do usuario",
            help="Nome completo do usuario."
        )
        senha = st.text_input(
                type='password',
                label="Digite sua senha",
                placeholder="Digite a senha",
                help="Senha de acesso do usuario."
            )
        email = st.text_input(
            label="E-mail",
            placeholder="Digite o email",
            help="Email do usuario."
            
        )
        adm = st.checkbox(
            label="É Administrador?",
            help="Marque se o usuario for administrador."
        )
        submit_button = st.form_submit_button(label="Salvar")
        cancel_button = st.form_submit_button(label="Cancelar")

    if submit_button:
            # Simulação de salvamento (substituir por lógica real)
            st.success(f"Usuario '{nome}' salva com sucesso!")
            salva_usuario(id=id, nome=nome, senha=senha, email=email, acesso_gestor=adm)
            st.rerun()

    elif cancel_button:
        st.warning("Cadastro cancelado!")

# Função principal para gerenciar a interface de usuários
def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        st.warning("Você precisa estar logado para acessar esta página.")
        return
    else:
        st.set_page_config(page_title="CAPACITA-Usuario", layout="wide", initial_sidebar_state="auto")
        usuario_logado = st.session_state['usuario']
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')

        # Exibir tabela de usuários para todos os logados
        with st.expander("Pesquisa de Usuarios", expanded=True):
            tabelaPaginada.show(df=buscar_todos_usuarios(), n_linhas_iniciais=5)

        # Exibir formulário apenas para administradores
        if usuario_logado.acesso_gestor:
            with st.expander("Cadastro de Usuarios", expanded=False):
                formUsuario()
        else:
            st.warning("Você não tem permissão para cadastrar novos usuários.")

        # Botão de logout
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()