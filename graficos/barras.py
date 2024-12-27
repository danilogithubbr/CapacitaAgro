import plotly.express as px

def show(df, x, y, titulo, legenda, categoria_cores):
    fig = px.bar(df, y=y, x=x, title=titulo, color=legenda, text_auto=True, color_discrete_map=categoria_cores)

    # Calcula o total geral por categoria
    df['total_geral'] = df.groupby(x)[y].transform('sum')

    # Adiciona uma linha para os totais gerais
    totais = df.groupby(x)['total_geral'].first().reset_index()  # Obtém os totais por categoria
    fig.add_scatter(
        x=totais[x],
        y=totais['total_geral'],
        mode='markers+text', # 'lines+markers+text'
        text=totais['total_geral'],
        textposition='top center',
        textfont=dict(size=15),
        name='',
        line=dict(color='rgba(255, 0, 0, 0)', dash='dash', width=2),  # Linha vermelha tracejada
        marker=dict(size=1, color='rgba(255, 0, 0, 0.3)')
    )

    # Obtém o valor máximo do eixo Y e adiciona uma margem
    max_y = df['total_geral'].max()
    margem = max_y * 0.15  # 15% de margem
    limite_superior = max_y + margem
    
#'lines+markers+text
    fig.update_layout(
        yaxis_title="", 
        xaxis_title="", 
        height=350, 
        plot_bgcolor="rgba(0,0,0,0)",  # parte interna do grafico
        paper_bgcolor="rgba(0,0,0,0)", # parte externa do grafico
        legend_title=dict(
            #text="Título da Legenda",  # Texto do título da legenda
            font=dict(size=11, color="black", family="Courier")  # Personalização do título da legenda
        ),
        legend=dict(
            font=dict(size=11, color="black", family="Courier New")  # Personalização dos itens da legenda
        )
        )
    
    fig.update_yaxes(
        range=[0, limite_superior], # Define o intervalo do eixo Y
        showgrid=False, # Remove as linhas da grade no eixo Y
        showticklabels=False,  # Remove os rótulos do eixo Y
        ) 
    
    fig.update_xaxes(
        tickfont=dict(size=15, color='black', family="Courier Bold")  # Define o tamanho e a cor dos rótulos do eixo X
    ) 
    return fig
