import streamlit as st
import pandas as pd
from time import sleep
from datetime import timedelta, date
from componentes import logout, tabelaPaginada

from model import buscar_todos_lancamentos, salva_lancamento, buscar_todos_treinamentos, buscar_treinamento, buscar_todos_colaboradores, buscar_detalhes_lancamento

df = buscar_todos_lancamentos()

def coluna_condicional(col):
        return [
             "background-color: red; color: white;" if v == "Atrasado" else 
             "background-color: yellow; color: black;" if v == "A Realizar" else 
             "background-color: green; color: white;" for v in col]

def formLancamento():
    
    if ("id_treinamento" not in st.session_state and "controle" not in st.session_state):
        st.session_state["id_lancamento"] = None
        st.session_state["id_treinamento"] = None
        st.session_state["controle"] = None

    if (st.session_state["id_treinamento"] is None or st.session_state["controle"] is None):    
        with st.form(key='form_filtro_lancamento'):

            dftr = buscar_todos_treinamentos()[['id_treinamento','nome']]
            opcoes_treinamentos = dftr.apply(lambda row: f"{row['id_treinamento']} - {row['nome']}", axis=1).tolist()
            mapa_treinamentos = dict(zip(opcoes_treinamentos, dftr['id_treinamento']))
            id_selecionado = st.selectbox(
                    label="ID Treinamento",
                    index=None,
                    options=opcoes_treinamentos,
                    help="Identificador único do treinamento."
                )
            if id_selecionado:
                id_treinamento =  mapa_treinamentos[id_selecionado]

            dfco = buscar_todos_colaboradores()[['controle','nome']]
            opcoes_colaboradores = dfco.apply(lambda row: f"{row['controle']} - {row['nome']}", axis=1).tolist()
            mapa_colaborador = dict(zip(opcoes_colaboradores, dfco['controle']))
            controle_selecionado = st.selectbox(
                    label="Controle",
                    index=None,
                    options=opcoes_colaboradores,
                    help="Identificador único do colaborador."
                )
            if controle_selecionado:
                controle =  mapa_colaborador[controle_selecionado]

            submit_button_filtro = st.form_submit_button(label="Editar")
        
        if submit_button_filtro:
                # Simulação de salvamento (substituir por lógica real)
                st.session_state["id_treinamento"] = id_treinamento
                st.session_state["controle"] = controle
                st.rerun()
    else:
        id_treinamento = int(st.session_state["id_treinamento"])
        controle = int(st.session_state["controle"])
        detalhes_df = buscar_detalhes_lancamento(id_treinamento, controle)
        id_lancamento = int(detalhes_df.iloc[0]["id_lancamento"]) if not detalhes_df.empty else None
        st.write(f"({id_lancamento}) => ID do Treinamento: {id_treinamento} - Controle do Colaborador: {controle}")
        # Renderização do formulário
        with st.form(key='form_lancamento'):

            data_validade = st.date_input(
                label="Data de Vencimento",
                value= detalhes_df.iloc[0]["data_validade"] if not detalhes_df.empty else date.today() + timedelta(days=60),
                format="DD/MM/YYYY",
                disabled=True,
                help="Selecione a data em que o treinamento foi realizado."
            )

            data_treinamento = st.date_input(
                label="Data do Treinamento",
                value=None, #detalhes_df.iloc[0]["data_treinamento"] if not detalhes_df.empty else None,
                format="DD/MM/YYYY",
                help="Selecione a data em que o treinamento foi realizado."
            )

            status = st.selectbox(
                label="Status",
                options=["Realizado", "Atrasado", "A Realizar", "Não Realizado"],
                index=["Realizado", "Atrasado", "A Realizar", "Não Realizado"].index(
                    detalhes_df.iloc[0]["status"] if not detalhes_df.empty else "Não Realizado"
                ),
                help="Status atual do colaborador."
            )
            submit_button = st.form_submit_button(label="Salvar")
            cancel_button = st.form_submit_button(label="Cancelar")

            if submit_button:

                    # Simulação de salvamento (substituir por lógica real)
                    if data_treinamento is not None:
                        salva_lancamento(id_lancamento=id_lancamento, id_treinamento=id_treinamento, controle=controle, data_validade=data_validade, data_treinamento=data_treinamento, status="Realizado")
                        st.success(f"Lançamento com data '{data_treinamento}' salvo com sucesso!")
                        sleep(1)
                        data_validade = data_treinamento + timedelta(days=float(buscar_treinamento(id_treinamento=id_treinamento)['dias_validade'].iloc[0]))
                        salva_lancamento(id_lancamento=None, id_treinamento=id_treinamento, controle=controle, data_validade=data_validade, data_treinamento=None, status="A Realizar") # Cria novo lançamento
                        st.success(f"Proximo Lançamento com data '{data_validade}' criado com sucesso!")
                        sleep(1)
                        st.session_state["id_treinamento"] = None
                        st.session_state["controle"] = None
                        st.rerun()
                    else:    
                        salva_lancamento(id_lancamento=id_lancamento, id_treinamento=id_treinamento, controle=controle, data_validade=data_validade, data_treinamento=data_treinamento, status="A Realizar")
                        st.success(f"Lançamento com data '{data_treinamento}' salvo com sucesso!")
                        sleep(1)
                        st.session_state["id_treinamento"] = None
                        st.session_state["controle"] = None
                        st.rerun()

            elif cancel_button:
                st.warning("Cadastro cancelado!")
                sleep(1)
                st.session_state["id_treinamento"] = None
                st.session_state["controle"] = None
                st.rerun()

# Função principal para gerenciar a interface de colaboradores
def main():
    if not 'logado' in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        st.warning("Você precisa estar logado para acessar esta página.")
        return
    else:
        usuario_logado = st.session_state['usuario']
        st.sidebar.write(f'Usuário logado: {usuario_logado.nome}')

        # Exibir a interface de pesquisa de funcoes
        with st.expander("Pesquisa de Treinamentos Realizados", expanded=True):
            tabelaPaginada.show(df=df, n_linhas_iniciais=5, colFiltro="status", diferenteDe="Realizado", label="Pendentes", funStyle=coluna_condicional, colStyle="status")

        # Exibir o formulário de cadastro de funcoes
        with st.expander("Lançamento de Treinamentos Realizados", expanded=True):
            formLancamento()
        
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()
