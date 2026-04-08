import streamlit as st
import pandas as pd
from components.layout import show_header
from database import run_query

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Gestão de Produtos")

@st.dialog("Cadastrar Novo Produto")
def modal_novo_produto():
    nome = st.text_input("Nome do Produto*")
    categoria = st.selectbox("Categoria", ["Skincare", "Maquiagem", "Cremes de Massagem", "Outros"])
    
    col1, col2 = st.columns(2)
    with col1:
        valor_custo = st.number_input("Valor de Custo (R$)", min_value=0.0, format="%.2f")
    with col2:
        valor_venda = st.number_input("Valor Estimado p/ Venda (R$)", min_value=0.0, format="%.2f")
        
    quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
    
    if st.button("Salvar Produto", use_container_width=True):
        if nome:
            query = """INSERT INTO produtos (nome, categoria, valor_custo, valor_venda_estimado, quantidade_estoque) 
                       VALUES (%s, %s, %s, %s, %s)"""
            sucesso = run_query(query, (nome, categoria, valor_custo, valor_venda, quantidade), fetch=False)
            if sucesso:
                st.success("Produto adicionado ao estoque!")
                st.rerun()
        else:
            st.warning("O Nome do produto é obrigatório.")

# -- BARRA DE AÇÕES E FILTROS --
col_busca, col_btn = st.columns([4, 1])
with col_busca:
    busca = st.text_input("🔍 Buscar produto por nome ou categoria...")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Novo Produto", use_container_width=True):
        modal_novo_produto()

# -- TABELA DE PRODUTOS --
if busca:
    query = "SELECT id, nome, categoria, valor_custo, valor_venda_estimado, quantidade_estoque FROM produtos WHERE nome ILIKE %s OR categoria ILIKE %s ORDER BY nome ASC"
    dados = run_query(query, (f"%{busca}%", f"%{busca}%"))
else:
    query = "SELECT id, nome, categoria, valor_custo, valor_venda_estimado, quantidade_estoque FROM produtos ORDER BY nome ASC"
    dados = run_query(query)

if dados:
    df = pd.DataFrame(dados)
    df.columns = ["ID", "Nome do Produto", "Categoria", "Custo (R$)", "Venda (R$)", "Qtd Estoque"]
    
    # Destaca produtos com estoque baixo (opcional, visual)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum produto cadastrado no estoque.")