import streamlit as st
import pandas as pd
from components.layout import show_header
from database import run_query

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Catálogo de Procedimentos")

@st.dialog("Cadastrar Novo Procedimento")
def modal_novo_procedimento():
    nome = st.text_input("Nome do Procedimento*")
    categoria = st.selectbox("Categoria", ["Facial", "Corporal", "Micropigmentação", "Sobrancelhas", "Outros"])
    valor = st.number_input("Valor de Atendimento (R$)", min_value=0.0, format="%.2f")
    duracao = st.number_input("Duração estimada (minutos)", min_value=15, step=15, value=60)
    
    if st.button("Salvar Procedimento", use_container_width=True):
        if nome:
            query = "INSERT INTO procedimentos (nome, categoria, valor_padrao, duracao_minutos) VALUES (%s, %s, %s, %s)"
            sucesso = run_query(query, (nome, categoria, valor, duracao), fetch=False)
            if sucesso:
                st.success("Procedimento cadastrado com sucesso!")
                st.rerun()
        else:
            st.warning("O Nome do procedimento é obrigatório.")

# -- BARRA DE AÇÕES E FILTROS --
col_busca, col_btn = st.columns([4, 1])
with col_busca:
    busca = st.text_input("🔍 Buscar procedimento...")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Novo Procedimento", use_container_width=True):
        modal_novo_procedimento()

# -- TABELA DE PROCEDIMENTOS --
if busca:
    query = "SELECT id, nome, categoria, valor_padrao, duracao_minutos FROM procedimentos WHERE nome ILIKE %s ORDER BY nome ASC"
    dados = run_query(query, (f"%{busca}%",))
else:
    query = "SELECT id, nome, categoria, valor_padrao, duracao_minutos FROM procedimentos ORDER BY nome ASC"
    dados = run_query(query)

if dados:
    df = pd.DataFrame(dados)
    df.columns = ["ID", "Procedimento", "Categoria", "Valor (R$)", "Duração (min)"]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum procedimento cadastrado.")