from time import sleep
from datetime import date
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from componentes import login, logout

# Configuração inicial da página
st.set_page_config(page_title="CAPACITA-AGRO", layout="wide")

def dashboard():
    custom_theme = {
        "layout": {
            "font": {"family": "Arial", "size": 16, "color": "white"},
            "paper_bgcolor": "#333",
            "plot_bgcolor": "#222",
            "title": {"x": 0.5, "font": {"size": 20, "color": "#FF5733"}}
        }
    }
    # Widgets para ajustar os parâmetros
    amplitude = st.slider("Amplitude", 1, 10, 5)
    frequencia = st.slider("Frequência", 1, 10, 3)

    # Dados do gráfico
    x = np.linspace(0, 10, 500)
    y = amplitude * np.sin(frequencia * x)

    # Criando o gráfico com Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Seno"))
    fig.update_layout(title="Gráfico Seno Interativo", xaxis_title="X", yaxis_title="Amplitude")
    fig.update_layout(template=custom_theme)

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        login.login()
    else:
        dashboard()
        usuario_logado = st.session_state['usuario']
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()

