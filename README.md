# 🗺️ MAP Turismo – Guia Turístico Inteligente de Brasília

Projeto desenvolvido com Streamlit, LangChain e OpenAI que utiliza arquivos em PDF e DOCX para responder perguntas sobre turismo em Brasília com base em fontes reais.

---

## ✅ Funcionalidades

- Chat interativo com interface moderna
- Leitura de documentos PDF, DOCX, TXT ou MD
- Vetorização automática com FAISS
- Histórico por sessão e exportação de conversa
- Respostas simpáticas e informativas com IA
- Contexto baseado em guias turísticos reais

---

## 🧩 Estrutura de Diretórios

oraculum/

├── main.py # Arquivo principal

├── views/ # Páginas do app

│ ├── chat_page.py

│ ├── upload_page.py

│ ├── faiss_page.py

│ └── qa_page.py

├── faiss_db.py # Módulo FAISS

├── utils.py # Histórico, conversão etc

├── file_md/ # Conversor docling

├── data/

│ └── md/ # PDFs e textos para ingestão

├── .env # Chaves da API

└── requirements.txt

---

## 💬 Exemplo de Uso
Pergunta: Quais são os principais parques de Brasília?

Resposta: (gerada com base no conteúdo dos PDFs)

Cita os nomes, características e fontes utilizadas como [GuiaParquesSeturDF.pdf].

---

## 📌 Observações
O horário exibido é baseado no fuso de Brasília (UTC-3)

Interface ajustada com balões e timestamps

Conversas podem ser exportadas via botão na barra lateral

---

## 🧠 Tecnologias Utilizadas
Python 3.10+

Streamlit

LangChain

OpenAI GPT-4o

FAISS

Docker

Docling

---

## 👨‍🏫 Projeto Acadêmico
Desenvolvido como entrega de projeto final para disciplina de IA aplicada.
Orientado para fornecer uma solução prática e acessível com uso de dados reais do turismo do DF.
