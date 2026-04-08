import streamlit as st
import requests
from components.layout import show_header

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

show_header("Assistente de IA - Paola Barletta")

st.markdown("💬 Converse com a inteligência artificial para buscar informações da agenda, clientes e resultados do banco de dados.")

# Memória do chat para manter a conversa na tela
if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = []

# Exibe o histórico do chat
for msg in st.session_state.mensagens_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de texto onde o usuário digita
pergunta = st.chat_input("Ex: Quais são os agendamentos de hoje?")

if pergunta:
    # 1. Mostra a mensagem do usuário na tela
    st.session_state.mensagens_chat.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
        
    # 2. Mostra um ícone de "pensando" enquanto o n8n trabalha
    with st.chat_message("assistant"):
        placeholder_resposta = st.empty()
        placeholder_resposta.markdown("⏳ Consultando o banco de dados...")
        
        try:
            # 3. Envia a pergunta para o SEU n8n local
            url_n8n = "http://localhost:5678/webhook-test/chat-ia"
            payload = {"pergunta": pergunta, "usuario_id": st.session_state.user_id}
            
            resposta = requests.post(url_n8n, json=payload, timeout=30)
            
            # 4. Pega a resposta gerada pelo n8n
            if resposta.status_code == 200:
                texto_ia = resposta.json().get("resposta", "Ação concluída no n8n.")
            else:
                texto_ia = f"Desculpe, não consegui conectar ao n8n (Status {resposta.status_code})."
                
        except Exception as e:
            texto_ia = "⚠️ O servidor n8n (Docker) parece estar desligado ou o webhook não foi criado ainda."

        # 5. Atualiza a tela com a resposta final
        placeholder_resposta.markdown(texto_ia)
        st.session_state.mensagens_chat.append({"role": "assistant", "content": texto_ia})