import streamlit as st
import base64
import os
from components.auth import hash_password, logout
from database import run_query

def get_base64_image(image_path):
    """Converte a imagem JPEG para base64 para o HTML entender"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

@st.dialog("Cadastrar Novo Usuário")
def modal_novo_usuario():
    st.write("Preencha os dados do novo acesso:")
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    role = st.selectbox("Nível de Acesso", ["USER", "ADMIN"])
    
    if st.button("Salvar Usuário", use_container_width=True):
        if nome e email e senha:
            senha_criptografada = hash_password(senha)
            query = "INSERT INTO usuarios (nome, email, senha_hash, role) VALUES (%s, %s, %s, %s)"
            sucesso = run_query(query, (nome, email, senha_criptografada, role), fetch=False)
            if sucesso:
                st.success(f"Usuário {nome} cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar. O e-mail já existe?")
        else:
            st.warning("Preencha todos os campos!")

def show_header(titulo_pagina):
    """Renderiza o cabeçalho no topo de cada página"""
    
    # 1. Pega as informações da sessão do usuário
    user_name = st.session_state.get("user_name", "Usuário")
    user_initial = user_name[0].upper() if user_name else "U"
    user_role = st.session_state.get("user_role", "USER")
    
    # 2. Prepara a logo
    logo_b64 = get_base64_image("assets/logo.jpeg")
    img_html = f'<img src="data:image/jpeg;base64,{logo_b64}" width="120" style="border-radius: 8px;">' if logo_b64 else "<h3>EPB</h3>"

    # 3. Desenha a estrutura (Usando colunas do Streamlit)
    col_logo, col_titulo, col_vazia, col_user, col_engrenagem = st.columns([2, 4, 2, 2, 1])
    
    with col_logo:
        st.markdown(img_html, unsafe_allow_html=True)
        
    with col_titulo:
        st.markdown(f"<h2 style='text-align: center; color: #333; margin-top: 15px;'>{titulo_pagina}</h2>", unsafe_allow_html=True)
        
    with col_user:
        # Foto/Inicial do usuário em formato oval/círculo
        st.markdown(f"""
            <div style='display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-top: 20px;'>
                <span style='font-weight: bold; color: #333;'>{user_name}</span>
                <div style='background-color: #E69AA8; color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold;'>
                    {user_initial}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_engrenagem:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        # O "popover" age como um menu dropdown na engrenagem
        with st.popover("⚙️"):
            if user_role == "ADMIN":
                if st.button("Novo Usuário", use_container_width=True):
                    modal_novo_usuario()
            if st.button("Sair / Logout", use_container_width=True):
                logout()
    
    st.divider() # Linha de separação abaixo do cabeçalho