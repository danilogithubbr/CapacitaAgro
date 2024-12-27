import plotly.graph_objects as go
import numpy as np

def criar_grafico(amplitude, frequencia, cor):
    x = np.linspace(0, 10, 500)
    y = amplitude * np.sin(frequencia * x)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=cor)))
    fig.update_layout(
        title=f"Gráfico Seno (Amplitude={amplitude}, Frequência={frequencia})",
        xaxis_title="X",
        yaxis_title="Y",
        template="plotly_dark",
    )
    return fig