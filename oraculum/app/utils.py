# utils.py

import tempfile
from typing import List
from pydantic import BaseModel, Field
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from docling.document_converter import DocumentConverter
import streamlit as st

from file_md import list_documents, get_document


# HISTÓRICO DE CONVERSA
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """
    Histórico de conversa armazenado em memória para cada sessão.
    """

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Adiciona múltiplas mensagens ao histórico."""
        self.messages.extend(messages)

    def clear(self) -> None:
        """Limpa todo o histórico de mensagens."""
        self.messages = []


# Armazena os históricos por session_id
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    """
    Recupera ou cria um histórico de conversa com base no session_id.
    """
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


# CONVERSÃO DE DOCUMENTO
def convert_file_to_md(uploaded_file):
    """
    Converte um arquivo enviado para markdown usando docling.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
        tmp.write(uploaded_file.read())
        temp_file_path = tmp.name

    converter = DocumentConverter()
    result = converter.convert(temp_file_path)
    return result.document.export_to_markdown()


# OBTÉM TEXTO DO DOCUMENTO SELECIONADO
def get_selected_document_text():
    """
    Retorna o conteúdo em texto do documento atualmente selecionado.
    """
    docs = list_documents()
    selected = st.session_state.get("selected_doc") or (docs[0] if docs else None)
    return get_document(selected) if selected else ""
