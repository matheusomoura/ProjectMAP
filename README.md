Guia de Implementação do Projeto Oraculum: Guia Turístico com IA

Este documento apresenta, em formato de passo a passo, todas as etapas realizadas para colocar em funcionamento o projeto Oraculum: um chatbot inteligente com RAG (Retrieval-Augmented Generation) especializado em turismo em Brasília, rodando com Streamlit e LangChain.

✅ 1. Estrutura Inicial do Projeto

Criamos a estrutura de pastas:

oraculum/
├─ app/
│   ├─ views/
│   └─ faiss_db.py, utils.py, main.py, etc.
├─ data/md/        # Pasta para PDFs e textos
├─ data/faiss_index/
└─ Dockerfile, docker-compose.yml

O arquivo docker-compose.yml definiu o container oraculum, com mapeamento de volume, variáveis .env, e porta 8501 do Streamlit.

✅ 2. Configuração de Ambiente

Criamos o .env com:

OPENAI_API_KEY=...
MODEL_CHAT=gpt-4o

Instalamos as dependências no requirements.txt:

streamlit
langchain
langchain-openai
python-dotenv
docling
faiss-cpu

✅ 3. Desenvolvimento das Páginas (views)

Criamos 4 views:

chat_page.py

upload_page.py

qa_page.py

faiss_page.py

Integramos no main.py com navegação via st.sidebar.radio

✅ 4. Interface do Chat

Implementamos layout com balões de conversa, scroll automático, timestamp, tema responsivo (removido depois)

Adicionamos opção de:

Exportar conversa em .txt

Limpar histórico de sessão

✅ 5. Vetorização e FAISS

O sistema converte arquivos PDF, DOCX, TXT ou MD para Markdown usando docling

Textos vetorizados com embeddings do LangChain + OpenAI

Armazenamento no diretório data/faiss_index/

✅ 6. Upload e Alimentação

Os arquivos são colocados na pasta:

oraculum/data/md/

Apesar do nome, aceita PDF, DOCX e TXT.

A conversão e indexação ocorre ao clicar no botão de upload ou ao reiniciar com arquivos novos.

✅ 7. Execução com Docker

Para iniciar o sistema:

docker-compose up --build

Para encerrar:

Basta pressionar Ctrl + C no terminal.

Para iniciar no dia seguinte:

docker-compose up

✅ Resultado Final

Sistema acessível em: http://localhost:8501

Chat responsivo e funcional

Respostas contextualizadas a partir dos documentos fornecidos

Pronto para ser usado por visitantes ou profissionais de turismo

✨ Extras

Sistema pode ser expandido para novos temas (educação, saúde, eventos)

Base local, sem necessidade de banco de dados

Pode ser hospedado em nuvem (Render, Railway, etc.)

