import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from components.layout import show_header
from database import run_query

# Verifica se está logado (proteção de rota)
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Agenda de Atendimentos")

# -- LÓGICA DE FINALIZAÇÃO (MODAL) --
@st.dialog("Finalizar Atendimento")
def modal_finalizar(agendamento_id, cliente_nome):
    st.write(f"Finalizando atendimento de: **{cliente_nome}**")
    
    obs = st.text_area("Observações sobre o atendimento")
    
    # Checkbox de Produtos
    vendeu_produto = st.checkbox("Venda de Produtos")
    if vendeu_produto:
        produtos = run_query("SELECT id, nome FROM produtos")
        if produtos:
            opcoes_prod = {p['nome']: p['id'] for p in produtos}
            prod_selecionado = st.selectbox("Selecione o Produto", list(opcoes_prod.keys()))
            qtd = st.number_input("Quantidade", min_value=1, step=1)
            valor_venda = st.number_input("Valor da Venda (R$)", min_value=0.0, format="%.2f")
        else:
            st.warning("Nenhum produto cadastrado.")

    # Checkbox de Procedimentos Extras
    fez_extra = st.checkbox("Agregação de Procedimentos (Extra)")
    if fez_extra:
        procedimentos = run_query("SELECT id, nome FROM procedimentos")
        if procedimentos:
            opcoes_proc = {p['nome']: p['id'] for p in procedimentos}
            proc_selecionado = st.selectbox("Selecione o Procedimento Extra", list(opcoes_proc.keys()))
            valor_extra = st.number_input("Valor do Procedimento (R$)", min_value=0.0, format="%.2f")
        else:
            st.warning("Nenhum procedimento cadastrado.")
            
    caixinha = st.number_input("Caixinha (R$)", min_value=0.0, format="%.2f")
    
    if st.button("Salvar Finalização", use_container_width=True):
        # Aqui entra a query de UPDATE no agendamento para 'Finalizado'
        run_query("UPDATE agendamentos SET status = 'Finalizado', observacoes = %s, caixinha = %s WHERE id = %s", (obs, caixinha, agendamento_id), fetch=False)
        st.success("Atendimento finalizado com sucesso!")
        st.rerun()

# -- TELA PRINCIPAL DA AGENDA --
col_data, col_btn = st.columns([3, 1])
with col_data:
    data_selecionada = st.date_input("Selecione a data para visualizar a agenda")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Novo Agendamento", use_container_width=True):
        st.info("O modal de novo agendamento com trava de horário será feito aqui.")

st.subheader(f"Agendamentos para {data_selecionada.strftime('%d/%m/%Y')}")

# Busca os agendamentos do dia no banco de dados
query_agenda = """
    SELECT a.id, c.nome AS cliente, p.nome AS procedimento, a.data_hora_inicio, a.data_hora_fim, a.status 
    FROM agendamentos a
    JOIN clientes c ON a.cliente_id = c.id
    JOIN procedimentos p ON a.procedimento_id = p.id
    WHERE DATE(a.data_hora_inicio) = %s
    ORDER BY a.data_hora_inicio ASC
"""
agendamentos = run_query(query_agenda, (data_selecionada,))

if not agendamentos:
    st.write("Nenhum atendimento marcado para este dia.")
else:
    for ag in agendamentos:
        hora_inicio = ag['data_hora_inicio'].strftime("%H:%M")
        hora_fim = ag['data_hora_fim'].strftime("%H:%M")
        
        # Cria um "card" visual para cada agendamento
        with st.container():
            st.markdown(f"### {hora_inicio} - {hora_fim} | {ag['cliente']}")
            st.write(f"**Procedimento:** {ag['procedimento']} | **Status:** {ag['status']}")
            
            # Lógica de mostrar o botão apenas se o horário já passou
            agora = datetime.now()
            if ag['status'] == 'Agendado' and agora >= ag['data_hora_fim']:
                if st.button(f"✅ Finalizar Atendimento", key=f"btn_{ag['id']}"):
                    modal_finalizar(ag['id'], ag['cliente'])
                    
            st.divider()