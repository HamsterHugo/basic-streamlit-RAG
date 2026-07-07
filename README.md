# Basic Streamlit RAG

A simple **Retrieval-Augmented Generation (RAG)** web application built with Streamlit that allows you to upload PDF documents, store them in a vector database, and ask questions about their content in a chat interface.

---

## ✨ Features

- **PDF Upload**: Upload one or multiple PDF documents.
- **Vector Database**: Automatically indexes documents using **FAISS** (Facebook AI Similarity Search).
- **Chat Interface**: Ask questions about the uploaded documents and receive precise answers based on their content.
- **Easy to Use**: No complex setup required – just upload, process, and chat.

---

## 🛠️ Technologies & Libraries

| Component        | Technology/Library               |
|------------------|-----------------------------------|
| **Frontend**     | Streamlit                         |
| **Backend**      | Python                            |
| **RAG Framework**| LangChain                         |
| **Vector Database** | FAISS (Facebook AI Similarity Search) |
| **PDF Processing** | PDFPlumber                      |
| **Language Model** | OpenAI **gpt-4o-mini**          |

---

## ⚠️ Prerequisites

To use this application, you need:
- An **OpenAI API key** (for accessing the `gpt-4o-mini` model).
- **Python 3.9+** (recommended: Python 3.14.2).
- **pip** (Python package manager).

---

## 📂 Project Structure
```
basic-streamlit-RAG/
├── fair_db/            # Folder for the FAISS vector database (created automatically)
├── uploaded_files/     # Folder for uploaded PDFs (created automatically)
├── .gitignore          # The gitignore file
├── chatbot.py          # Main Streamlit application
├── README.md           # This file
└── requirements.txt    # Dependencies
```

---

## 📥 Installation

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/HamsterHugo/basic-streamlit-RAG.git
   cd basic-streamlit-RAG
   ```

2. **Set up a virtual environment (optional but recommended):**
    ```python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt

    ```

4. **Set up your Open AI API key**
Create an environment variable named `OPEN_AI_API_KEY` and store your Open AI API key there.

---

## 🚀 **Usage**

1. **Start the application**
    Run the following command to start the streamlit app:
    ```
    streamlit run chatbot.py
    ```

2. **Upload PDF documents**
    * Open the app in your brwoser: `http://localhost:8501`.
    * Upload one or more PDF documents.

3. **Ask questions**
    * Enter a question about the uploaded documents in the chat.
    * The app will search the vector database and return an answer based on the document content.

4. **Close the app**
    Press `ctrl+C` in your terminal to end the app.