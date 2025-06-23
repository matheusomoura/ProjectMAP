import streamlit as st
from uuid import uuid4
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from utils import get_by_session_id
from faiss_db import search_documents
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz
import time

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_CHAT = os.getenv("MODEL_CHAT")


def clear_session_id():
    if "session_id_chat" in st.session_state:
        get_by_session_id(st.session_state.session_id_chat).clear()
        st.session_state.session_id_chat = None


def load_llm():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um guia turístico simpático, detalhista e especializado em Brasília. Use o conteúdo abaixo para responder perguntas dos visitantes com clareza e entusiasmo:

{context}

Se o contexto não for relevante para a pergunta, diga que não há informações disponíveis nos documentos. Sempre cite a fonte usando [NOME_DO_ARQUIVO] ao final da frase relevante."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    return prompt | ChatOpenAI(
        api_key=OPENAI_API_KEY,
        temperature=0.5,
        model=MODEL_CHAT,
        streaming=True
    )


def show():
    bubble_bot = "#e5e5ea"
    bubble_user = "#007aff"
    bg_color = "#f8f9fa"
    page_bg = "#ffffff"
    text_color = "#000000"
    input_bg = "#f1f1f1"
    input_border = "#ccc"
    text_bot = "#222"
    text_user = "white"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {page_bg} !important;
        color: {text_color} !important;
    }}

    .block-container, .stChatMessageInputContainer, .stTextInput, .stTextArea {{
        background-color: {page_bg} !important;
        color: {text_color} !important;
    }}

    .stChatMessageInputContainer input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {input_border} !important;
    }}

    .stDownloadButton > button, .stButton > button {{
        background-color: #f0f0f0 !important;
        color: {text_color} !important;
        border: none !important;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }}

    .stDownloadButton > button:hover, .stButton > button:hover {{
        background-color: #e0e0e0 !important;
    }}

    .chat-container {{
        max-height: 65vh;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 1rem;
        background-color: {bg_color};
        margin-bottom: 1rem;
    }}
    .message {{ display: flex; margin-bottom: 1rem; }}
    .message.user {{ justify-content: flex-end; }}
    .message.bot {{ justify-content: flex-start; }}
    .bubble {{
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        max-width: 75%;
        font-size: 1rem;
        line-height: 1.5;
        word-wrap: break-word;
    }}
    .message.user .bubble {{ background-color: {bubble_user}; color: {text_user}; border-bottom-right-radius: 0; }}
    .message.bot .bubble {{ background-color: {bubble_bot}; color: {text_bot}; border-bottom-left-radius: 0; }}
    .bubble .timestamp {{ font-size: 0.7rem; text-align: right; opacity: 0.6; margin-top: 4px; }}
    .blinking-cursor {{ animation: blink 1s steps(2, start) infinite; }}
    @keyframes blink {{ to {{ visibility: hidden; }} }}
    #chat-end {{ height: 1px; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("# 🗺️ Guia Interativo de Turismo em Brasília")
    st.caption("Descubra os encantos da capital com IA e aproveite roteiros turísticos criados a partir de fontes confiáveis.")

    if not st.session_state.get("session_id_chat"):
        st.session_state.session_id_chat = str(uuid4())

    chain = load_llm()
    history = get_by_session_id(st.session_state.session_id_chat)

    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in history.messages[-20:]:
            sender = "user" if msg.type == "human" else "bot"
            timestamp = getattr(msg, "metadata", {}).get("timestamp", datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%H:%M"))
            st.markdown(f"""
                <div class="message {sender}">
                    <div class="bubble">
                        {msg.content}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('<div id="chat-end"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Digite sua pergunta...")

    if prompt:
        timestamp = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%H:%M")
        human_message = HumanMessage(content=prompt)
        human_message.metadata = {"timestamp": timestamp}
        history.add_messages([human_message])

        st.markdown(f"""
            <div class="message user">
                <div class="bubble">
                    {prompt}
                    <div class="timestamp">{timestamp}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        try:
            docs = search_documents(prompt, k=10)
            context = ""
            for i, (doc, score) in enumerate(docs):
                source = doc.metadata.get("source", "Fonte desconhecida")
                context += f"**Fonte {i + 1} ({source})**: {doc.page_content}\n\n"
        except Exception as e:
            st.error(f"Erro na busca de contexto: {str(e)}")
            context = "Nenhum contexto encontrado."

        chat_history = history.messages[:-1]
        response_placeholder = st.empty()
        full_response = ""

        with st.spinner("Gerando sua experiência turística personalizada..."):
            try:
                for chunk in chain.stream({"question": prompt, "history": chat_history, "context": context}):
                    if content := getattr(chunk, 'content', ''):
                        full_response += content
                        response_placeholder.markdown(f"""
                            <div class='message bot'>
                                <div class='bubble'>
                                    <span>{full_response}</span><span class="blinking-cursor">▌</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.02)

                timestamp_bot = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%H:%M")
                response_placeholder.markdown(f"""
                    <div class='message bot'>
                        <div class='bubble'>
                            {full_response}
                            <div class='timestamp'>{timestamp_bot}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                ai_msg = AIMessage(content=full_response)
                ai_msg.metadata = {"timestamp": timestamp_bot}
                history.add_messages([ai_msg])

            except Exception as e:
                response_placeholder.empty()
                st.error(f"Erro na resposta: {str(e)}")
                history.add_messages([AIMessage(content="Desculpe, ocorreu um erro interno.")])

        st.rerun()