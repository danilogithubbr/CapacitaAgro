from time import sleep
import streamlit as st


def logout():
    st.session_state['logado'] = False
    st.session_state['usuario'] = None
    st.success('Você foi deslogado com sucesso!')
    st.rerun()

