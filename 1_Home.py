from time import sleep
from datetime import date
import streamlit as st

from model import le_todos_usuarios
from componentes import login, logout


# Configuração inicial da página
st.set_page_config(page_title="CAPACITA-AGRO", layout="wide")


def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        login.login()
    else:
        usuario_logado = st.session_state['usuario']
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()

