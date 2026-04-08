import streamlit as st
import bcrypt
from database import run_query

def hash_password(password):
    """
    Recebe a senha em texto puro digitada no primeiro cadastro e 
    transforma em um código criptografado irreversível.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """
    Compara a senha digitada no login com o código criptografado salvo no banco de dados.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def autenticar_usuario(email, senha):
    """
    Busca o e-mail no banco Neon. Se existir, valida a senha.
    Se tudo estiver correto, salva as informações do usuário na sessão do navegador.
    """
    # Query SQL para buscar o usuário pelo email
    query = "SELECT id, nome, email, senha_hash, role FROM usuarios WHERE email = %s"
    
    # Chama a função run_query (que criaremos no database.py) enviando a query e o email
    resultado = run_query(query, (email,))

    # Se o banco retornar algum dado (o email existe)
    if resultado:
        usuario = resultado[0] # Pega a primeira linha do resultado
        
        # Verifica se a senha digitada bate com a hash salva no banco
        if check_password(senha, usuario['senha_hash']):
            
            # st.session_state é a memória do Streamlit. 
            # Guardamos essas informações para usar nas outras telas do sistema.
            st.session_state.logged_in = True
            st.session_state.user_id = usuario['id']
            st.session_state.user_name = usuario['nome']
            st.session_state.user_role = usuario['role'] # 'ADMIN' ou 'USER'
            
            return True # Login com sucesso
            
    return False # Email não encontrado ou senha incorreta

def logout():
    """
    Limpa a memória do navegador e força o usuário a voltar para a tela de login.
    """
    # Apaga todas as chaves salvas na sessão atual
    for key in list(st.session_state.keys()):
        del st.session_state[key]
        
    st.session_state.logged_in = False
    st.rerun() # Atualiza a página imediatamente