import os
import hashlib

import pdfplumber
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

# Load the api key for open ai
OPEN_AI_API_KEY: str = os.environ["OPEN_AI_API_KEY"]

DB_DIR: str = "fair_db"
UPLOADED_FILES_DIR: str = "uploaded_files"

os.makedirs(UPLOADED_FILES_DIR, exist_ok=True)

# Building the page header and file uploader
st.header("My First Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader(
        "Upload a PDF file and start asking questions", type="pdf"
    )

def get_file_hash(uploaded_file):
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    return hashlib.md5(file_bytes).hexdigest()

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

#generating embeddings
embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small",
    openai_api_key = OPEN_AI_API_KEY
)

if os.path.exists(DB_DIR):
    vector_store = FAISS.load_local(
        DB_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    vector_store = None

if file is not None:
    file_hash = get_file_hash(file)
    saved_pdf_path = os.path.join(UPLOADED_FILES_DIR, f"{file_hash}.pdf")
    is_new_file = not os.path.exists(saved_pdf_path)

    if is_new_file:
        with open(saved_pdf_path, "wb") as saved_file:
            saved_file.write(file.getbuffer())

        #extract text from it
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        #Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "source": file.name,
                    "file_hash": file_hash
                }
            )
            for chunk in chunks
        ]

        #new_vector_store = FAISS.from_documents(documents, embeddings)

        if documents:
            new_vector_store = FAISS.from_documents(documents, embeddings)
        
            if vector_store is None:
                vector_store = new_vector_store
            else:
                vector_store.merge_from(new_vector_store)
        
            vector_store.save_local(DB_DIR)
            st.success("PDF data saved to database.")
        else:
            st.warning("No readable text was found in this PDF.")
    else:
        st.info("This PDF is already saved in the database.")

    #store embeddings in vector db
    #vector_store = FAISS.from_texts(chunks, embeddings)

#get user question
user_question = st.text_input("Type your question here")

if vector_store is not None:
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=500,
        openai_api_key=OPEN_AI_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
        "You are a helpful assistant answering questions about uploaded PDF documents.\n\n"
        "Guidelines:\n"
        "1. Provide complete, well-explained answers using the context below.\n"
        "2. Include relevant details, numbers, and explanations.\n"
        "3. Only use information from the provided context.\n"
        "4. If the information is not in the context, say so politely.\n\n"
        "Context:\n{context}"),
        ("human", "{question}")
    ])

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    if user_question:
        response = chain.invoke(user_question)
        st.write(response)
else:
    st.warning("Upload at least one PDF to create the database.")