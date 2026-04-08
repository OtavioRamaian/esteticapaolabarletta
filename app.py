import streamlit as st
import base64
import os
from components.auth import autenticar_usuario

# A configuração da página DEVE ser a primeira linha do app.py
st.set_page_config(
    page_title="Login - Estética Paola Barletta",
    page_icon="🌸",
    layout="centered"
)

# Se já estiver logado, pula o login e vai direto para a Home
if st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def login_page():
    # Estilização para centralizar e embelezar o login
    st.markdown("""
        <style>
        .login-box {
            background-color: #FFF0F3;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Colocando a logo no topo do login
        logo_b64 = get_base64_image("assets/logo.jpeg")
        if logo_b64:
            st.markdown(f"<div style='text-align: center;'><img src='data:image/jpeg;base64,{logo_b64}' width='180' style='border-radius: 10px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #333;'>Acesso Restrito</h2>", unsafe_allow_html=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        
        with st.form("form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if email and senha:
                    if autenticar_usuario(email, senha):
                        st.success("Login efetuado com sucesso!")
                        st.switch_page("pages/home.py")
                    else:
                        st.error("Credenciais inválidas. Tente novamente.")
                else:
                    st.warning("Preencha todos os campos.")
                    
        st.markdown("</div>", unsafe_allow_html=True)

# Renderiza a tela de login
login_page()