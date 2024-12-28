from time import sleep
from datetime import date
#import locale
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import pandas as pd
from componentes import login, logout
from graficos import barras, trace
from model import buscar_todos_lancamentos

#locale.setlocale(locale.LC_ALL, 'pt_BR')

if 'logado' not in st.session_state:
        st.session_state['logado'] = False

if not st.session_state['logado']:
        st.set_page_config(page_title="CAPACITA-AGRO", layout="wide", initial_sidebar_state="auto")
else:
    st.set_page_config(page_title="CAPACITA-AGRO", initial_sidebar_state="collapsed")

#block-container
def ordena_mes(mes):
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    return meses.index(mes)
def ordena_processo(processo):
    processos = ['Plantio', 'Tratos', 'Colheita', 'Manutenção', 'Qualidade', 'Serviços Agr.']
    return processos.index(processo)

def dashboard():
    st.markdown("""
                <style>
                /* Ajustar margens e paddings da página */
                .block-container {
                    /* height: 100vh; */
                    padding-top: 1rem; /* Ajuste conforme necessário */
                    padding-bottom: 1rem;
                    max-width: 100%;
                    background: linear-gradient(180deg, #d3efbf, #def3cf, #ffffff, #f4fbef, #e9f7df);
                    background-attachment: fixed;
                    border-radius: 8px;
                }
                </style>
                """, unsafe_allow_html=True)
    df1 = buscar_todos_lancamentos()
    df2 = df1[df1["status"] != "Realizado"]
    df2["mes"] = df2['data_validade'].apply(lambda x: x.strftime('%B'))
    df2["ano"] = df2['data_validade'].apply(lambda x: x.year).astype(int)
    anos = df2['ano'].unique()
    #st.divider()
    colTitulo, colFiltro = st.columns(spec=[0.7,0.3], gap="large", vertical_alignment="top")
    with colTitulo:
        st.title("Capacita-Agro | Acompanhamento Treinamentos")
    with colFiltro:
         selected_ano = st.radio('Selecione o ano', anos, horizontal=True)
    df = df2[df2["ano"] == selected_ano]
    copiadf = df.groupby(["status","processo"]).size().reset_index(name="quantidade")
    pendenteMes = df.groupby(["mes","processo"]).size().reset_index(name="quantidade")
    #st.divider()
    status_cores = {
        "Atrasado": "red",  # Vermelho
        "A Realizar": "#FFFF00",  # amarelo
        "Colheita": "#3357FF",  # Azul
        "Plantio": "#672600",  # Marrom
        "Tratos": "#9d53a9", # Roxo
        "Qualidade": "#007100", # Verde
        "Manutenção": "#67594e", # Cinza
        "Serviços Agr.": "#FF5733", #Laranja

    }

    col1, col2 = st.columns(spec=[0.25,0.75], gap="small", vertical_alignment="top")
    with col1:
        st.plotly_chart(barras.show(
            df=copiadf, 
            x="status", 
            y="quantidade",
            titulo="Treinamentos Por Status",
            legenda="processo",
            categoria_cores=status_cores), 
            key="col1", use_container_height=True)
    with col2:
        st.plotly_chart(barras.show(
            df=copiadf.sort_values(by="processo", key=lambda x: x.apply(ordena_processo)), 
            x="processo", 
            y="quantidade",
            titulo="Treinamentos Por Processo",
            legenda="status",
            categoria_cores=status_cores), 
            key="col2", use_container_height=True)
        
    col3, col4, col5 = st.columns(spec=[0.01, 0.98,0.01], gap="small", vertical_alignment="top")
    with col4:
        st.plotly_chart(barras.show(
            df=pendenteMes.sort_values(by="mes", key=lambda x: x.apply(ordena_mes)), 
            x="mes", 
            y="quantidade",
            titulo="Treinamentos A Realizar",
            legenda="processo",
            categoria_cores=status_cores), 
            key="col4", use_container_height=True)






    
def main():
    if not st.session_state['logado']:
        #st.set_page_config(page_title="CAPACITA-AGRO", layout="wide", initial_sidebar_state="auto")
        login.login()
    else:
        dashboard()

        usuario_logado = st.session_state['usuario']
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()

