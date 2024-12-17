from time import sleep
import streamlit as st

from model import le_todos_usuarios


def logout():
    st.session_state['logado'] = False
    st.session_state['usuario'] = None
    st.success('Você foi deslogado com sucesso!')
    st.rerun()

