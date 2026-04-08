import streamlit as st
import pandas as pd
from components.layout import show_header
from database import run_query

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Histórico Geral")

# Filtro de data global para o histórico
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data Inicial")
with col2:
    data_fim = st.date_input("Data Final")

# Cria as duas abas na mesma tela
aba_procedimentos, aba_vendas = st.tabs(["💆‍♀️ Histórico de Procedimentos", "🛍️ Histórico Vendas de Produtos"])

with aba_procedimentos:
    st.subheader("Atendimentos Finalizados")
    query_proc = """
        SELECT a.data_hora_inicio::date as data, c.nome as cliente, p.nome as procedimento, a.valor_final, a.caixinha, a.observacoes 
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN procedimentos p ON a.procedimento_id = p.id
        WHERE a.status = 'Finalizado' AND a.data_hora_inicio::date BETWEEN %s AND %s
        ORDER BY a.data_hora_inicio DESC
    """
    dados_proc = run_query(query_proc, (data_inicio, data_fim))
    
    if dados_proc:
        df_proc = pd.DataFrame(dados_proc)
        df_proc.columns = ["Data", "Cliente", "Procedimento", "Valor Cobrado (R$)", "Caixinha (R$)", "Observações"]
        st.dataframe(df_proc, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum procedimento finalizado neste período.")

with aba_vendas:
    st.subheader("Produtos Vendidos")
    query_vendas = """
        SELECT vp.data_venda::date as data, p.nome as produto, vp.quantidade, vp.valor_unitario, (vp.quantidade * vp.valor_unitario) as total
        FROM vendas_produtos vp
        JOIN produtos p ON vp.produto_id = p.id
        WHERE vp.data_venda::date BETWEEN %s AND %s
        ORDER BY vp.data_venda DESC
    """
    dados_vendas = run_query(query_vendas, (data_inicio, data_fim))
    
    if dados_vendas:
        df_vendas = pd.DataFrame(dados_vendas)
        df_vendas.columns = ["Data", "Produto", "Qtd", "Valor Unitário (R$)", "Total (R$)"]
        st.dataframe(df_vendas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma venda registrada neste período.")