import streamlit as st

# ✅ Deve ser o primeiro comando do script
st.set_page_config(
    page_title="MAP Turismo",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

import torch
from views import upload_page, chat_page, faiss_page, qa_page
from faiss_db import init_faiss_index
from utils import get_by_session_id  # necessário para limpar e exportar

# Corrige possível erro com Torch em contêineres minimalistas
torch.classes.__path__ = []

def main():
    init_faiss_index()

    if "session_id_chat" not in st.session_state:
        st.session_state["session_id_chat"] = None

    def clear_session_id():
        if st.session_state["session_id_chat"]:
            get_by_session_id(st.session_state["session_id_chat"]).clear()
            st.session_state["session_id_chat"] = None

    with st.sidebar:
        st.markdown("""
            <style>
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.5rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .sidebar-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 1.2rem;
            }
            .sidebar-section {
                margin-bottom: 2rem;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-title'>🗂️ MAP Turismo</div>", unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        page = st.radio("Navegue pelo app:",
                        ["💬 Chat com RAG", "📤 Upload e Processamento", "🧠 Gerador QA", "📂 FAISS Manager"],
                        label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Opções do Chat")

        st.button("🧹 Limpar Conversa", on_click=clear_session_id)

        if st.session_state.get("session_id_chat"):
            history = get_by_session_id(st.session_state["session_id_chat"])
            export_text = "\n\n".join(f"{m.type.upper()}: {m.content}" for m in history.messages)
            st.download_button("📄 Exportar conversa (.txt)", export_text, "conversa_turismo.txt", "text/plain")

    # Roteia a página
    if page == "📤 Upload e Processamento":
        upload_page.show()
    elif page == "📂 FAISS Manager":
        faiss_page.show_faiss_manager()
    elif page == "🧠 Gerador QA":
        qa_page.show_qa_generator()
    else:
        chat_page.show()

if __name__ == "__main__":
    main()
