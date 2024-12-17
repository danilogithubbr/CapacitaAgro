import streamlit as st
from datetime import date
from time import sleep
from model import buscar_todos_colaboradores, buscar_todas_funcoes, buscar_todos_procesos, salva_colaborador
from componentes import logout, tabelaPaginada

df = buscar_todos_colaboradores()
# Função para exibir o formulário de cadastro de colaborador
def formColaborador():
    st.markdown("## Cadastro de Colaborador")
    with st.form(key='form_colaborador'):
        controle = st.number_input(
            label="Controle",
            min_value=1,
            value=len(df) + 1,
            format="%d",
            help="Identificador único do colaborador."
        )

        nome = st.text_input(
            label="Nome",
            placeholder="Digite o nome do colaborador",
            help="Nome completo do colaborador."
        )

        posicao = st.selectbox(
            label="Nº Posição",
            options=buscar_todas_funcoes()["posicao"], 
            help="Selecione a função do colaborador."
        )

        cdc = st.selectbox(
            label="Centro de Custo",
            options=buscar_todos_procesos()["cdc"],
            help="Selecione o centro de custo relacionado ao colaborador."
        )

        prazo = st.date_input(
            label="Data Fim Contrato",
            min_value=date.today(),
            help="Data limite para a tarefa ou treinamento."
        )

        status = st.selectbox(
            label="Status",
            options=["Ativo", "Inativo"],
            help="Status atual do colaborador."
        )

        submit_button = st.form_submit_button(label="Salvar")
        cancel_button = st.form_submit_button(label="Cancelar")

    # Ações ao enviar o formulário
    if submit_button:
            # Simulação de salvamento (substituir por lógica real)
            salva_colaborador(controle=controle, nome=nome, posicao=posicao, cdc=cdc, prazo=prazo, status=status)
            st.success(f"Colaborador '{nome}' salvo com sucesso!")
            sleep(1)
            st.rerun()


    elif cancel_button:
        st.warning("Cadastro cancelado!")

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
        with st.expander("Pesquisa de Colaborador", expanded=True):
            tabelaPaginada.show(df=df, n_linhas_iniciais=5, colFiltro="status", diferenteDe="Inativo", label="Ativos")
        # Exibir o formulário de cadastro de funcoes
        with st.expander("Cadastro de Colaborador", expanded=False):
            formColaborador()
        
        if st.sidebar.button('Logout'):
            logout.logout()

if __name__ == '__main__':
    main()
