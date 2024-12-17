import streamlit as st
import pandas as pd

def show(df, n_linhas_iniciais=5, colFiltro=None, diferenteDe=None, label=None, funStyle=None, colStyle=None):

    if df.empty:
        st.warning("O DataFrame está vazio. Nenhum dado para exibir.")
        return
    
    if diferenteDe is not None:
        coluna_filtro_geral = st.checkbox(f"Somente {label}", value=True)
        df = df[df[colFiltro] != diferenteDe] if coluna_filtro_geral is True else df

    coluna_filtro = st.selectbox("Filtrar por:", df.columns)
    valor_filtro = st.text_input(f"Digite o valor para filtrar em {coluna_filtro}")
    
    
    try:
        # Aplicar o filtro dependendo do tipo da coluna
        if valor_filtro.strip():  # Se o filtro não estiver vazio
            if df[coluna_filtro].dtype == 'object':  # Se for string
                df_filtrado = df[df[coluna_filtro].str.contains(valor_filtro, na=False, case=False)]
            else:  # Se for numérico
                valor_filtro_num = float(valor_filtro)
                df_filtrado = df[df[coluna_filtro] == valor_filtro_num]
        else:
            df_filtrado = df  # Exibir todos os dados se o filtro estiver vazio
    except ValueError:
        df_filtrado = pd.DataFrame()  # Tabela vazia no caso de erro de conversão

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para o filtro aplicado.")
        return
    
    # Configurar linhas visíveis no estado da sessão
    if "linhas_visiveis" not in st.session_state:
        st.session_state.linhas_visiveis = n_linhas_iniciais

    # Obter as linhas visíveis
    linhas_a_exibir = df_filtrado.head(st.session_state.linhas_visiveis)

    # Tamanho máximo de linhas a serem mostradas
    max_linhas = len(df_filtrado)      
    
    # aplicar estilos nas linhas
    #styled_df = linhas_a_exibir.style.set_properties( **{'background-color': '#f9f9f9'}, subset=pd.IndexSlice[::2, :]  # Linhas ímpares
    #                                ).set_properties(**{'background-color': '#f1f1f1'}, subset=pd.IndexSlice[1::2, :])  # Linhas pares
    if funStyle:
        styled_df = linhas_a_exibir.style.apply(funStyle, subset=[colStyle], axis=0)
    else:
        styled_df = linhas_a_exibir

    st.dataframe(styled_df) 

    # Mostrar botão "Ver mais"
    if st.session_state.linhas_visiveis < max_linhas:
        if st.button("Ver mais"):
            st.session_state.linhas_visiveis = min(st.session_state.linhas_visiveis + n_linhas_iniciais, max_linhas)
            st.rerun()  # Atualiza a tabela com as novas linhas

    # Mostrar botão "Ver menos"
    if st.session_state.linhas_visiveis > n_linhas_iniciais:
        if st.button("Ver menos"):
            st.session_state.linhas_visiveis = max(st.session_state.linhas_visiveis - n_linhas_iniciais, n_linhas_iniciais)
            st.rerun()  # Atualiza a tabela com as linhas reduzidas