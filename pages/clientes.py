import streamlit as st
import pandas as pd
from components.layout import show_header
from database import run_query

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Gestão de Clientes")

@st.dialog("Cadastrar Novo Cliente")
def modal_novo_cliente():
    nome = st.text_input("Nome do Cliente*")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        captacao = st.selectbox("Captação (Origem)", ["Instagram", "WhatsApp", "Indicação", "Outros"])
    with col2:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    with col3:
        sexo = st.selectbox("Sexo", ["F", "M"])
        
    if st.button("Salvar Cliente", use_container_width=True):
        if nome:
            query = """INSERT INTO clientes (nome, telefone, email, captacao, idade, sexo) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            sucesso = run_query(query, (nome, telefone, email, captacao, idade, sexo), fetch=False)
            if sucesso:
                st.success("Cliente cadastrado!")
                st.rerun()
        else:
            st.warning("O Nome do cliente é obrigatório.")

# -- BARRA DE AÇÕES E FILTROS --
col_busca, col_btn = st.columns([4, 1])
with col_busca:
    busca = st.text_input("🔍 Buscar cliente por nome ou telefone...")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Novo Cliente", use_container_width=True):
        modal_novo_cliente()

# -- TABELA DE CLIENTES --
# Monta a query baseada na busca (Filtro)
if busca:
    query_clientes = "SELECT id, nome, telefone, email, captacao, idade, sexo FROM clientes WHERE nome ILIKE %s OR telefone ILIKE %s ORDER BY nome ASC"
    dados = run_query(query_clientes, (f"%{busca}%", f"%{busca}%"))
else:
    query_clientes = "SELECT id, nome, telefone, email, captacao, idade, sexo FROM clientes ORDER BY id DESC LIMIT 50"
    dados = run_query(query_clientes)

if dados:
    # Usando o Pandas para deixar a tabela visualmente bonita no Streamlit
    df = pd.DataFrame(dados)
    # Renomeando as colunas para ficar elegante
    df.columns = ["ID", "Nome", "Telefone", "E-mail", "Captação", "Idade", "Sexo"]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum cliente encontrado.")