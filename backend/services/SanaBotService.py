import os
import re
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from datetime import datetime
import json
from bson import ObjectId
from config import GROQ_API_KEY, MONGO_URI, MONGO_DB

PERSIST_DIRECTORY = "./chroma_db_v2"
DATA_PATH = "./ChatbotData"

conversational_rag_chain = None

def get_session_history(session_id: str):
    return MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=session_id,
        database_name=MONGO_DB,
        collection_name="chat_histories"
    )

def initialize_chatbot():
    global conversational_rag_chain
    print("[INIT] Inicializando Sana Bot (Groq + RAG)...")
    api_key = GROQ_API_KEY
    if not api_key:
        print("[WARN] ADVERTENCIA: GROQ_API_KEY no encontrada.")
        return

    llm = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile", temperature=0.3)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print("[INFO] Cargando base de datos vectorial existente...")
        vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    else:
        print("[INFO] Procesando documentos médicos y de seguros...")
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
        loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        docs = loader.load()
        if not docs:
            vectorstore = Chroma(embedding_function=embeddings, persist_directory=PERSIST_DIRECTORY)
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
            print("[OK] Documentos procesados.")

    retriever = vectorstore.as_retriever()

    contextualize_q_system_prompt = (
        "Dada una historia de chat y la última pregunta del usuario "
        "que podría hacer referencia al contexto en la historia del chat, "
        "formula una pregunta independiente que pueda entenderse sin la historia del chat. "
        "NO respondas a la pregunta, solo reformúlala si es necesario."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    system_prompt = (
        "Te llamas Sana. Eres un agente conversacional de la aplicación MediByte. "
        "Tu objetivo principal es ayudar al paciente a entender su beneficio antes de atenderse. "
        "El paciente ingresará un síntoma (por ejemplo: 'Me duele la cabeza' o 'Me torcí el tobillo'). "
        "Debes analizar su caso y estructurar tu respuesta de la siguiente manera: \n"
        "1. Especialidad recomendada: Sugiere la especialidad médica adecuada para el síntoma.\n"
        "2. Cobertura: Analiza las reglas de cobertura del plan de seguro del paciente y dile explícitamente SI CUBRE O NO CUBRE la especialidad recomendada.\n"
        "3. Copago y Reembolsos: Indícale exactamente de cuánto será su copago si usa la red. Además, explícale cómo funciona el reembolso en su plan si decide ir a un hospital fuera de la red.\n"
        "4. Hospital recomendado: Sugiérele el hospital de su red preferida que más le convenga.\n\n"
        "*** IMPORTANTE: El paciente tiene actualmente contratado el {insurance_plan}. ***\n"
        "Debes basar tu decisión de cobertura, copagos y reembolsos ÚNICAMENTE en las reglas de este plan.\n\n"
        "Si no sabes la respuesta o no está en el contexto, sé honesto. "
        "Sé empática, clara, y amigable.\n\n"
        "Contexto de planes de seguro y red de hospitales:\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    print("[OK] Sana Bot lista.")

class SanaBotService:
    def __init__(self, db):
        self.db = db

    async def get_chat_messages(self, session_id: str):
        messages = []
        cursor = self.db["chat_histories"].find({"SessionId": session_id}).sort("_id", 1)
        async for doc in cursor:
            try:
                if "History" in doc:
                    msg_content = json.loads(doc["History"])
                    messages.append({
                        "type": msg_content["type"],
                        "content": msg_content["data"]["content"]
                    })
            except Exception as e:
                print(f"Error parseando mensaje: {e}")
                continue
        return messages

    async def chat_with_bot(self, message: str, session_id: str, user_id: str, insurance_plan: str = "Plan Base"):
        global conversational_rag_chain
        if conversational_rag_chain is None:
            initialize_chatbot()
        
        response = conversational_rag_chain.invoke(
            {"input": message, "insurance_plan": insurance_plan},
            config={"configurable": {"session_id": session_id}},
        )
        return response["answer"]

    def _preparar_texto_tts(self, texto: str) -> str:
        texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
        texto = re.sub(r'\*(.*?)\*', r'\1', texto)
        texto = re.sub(r'#+\s*', '', texto)
        texto = re.sub(r'`(.*?)`', r'\1', texto)
        texto = re.sub(r'\n+', '. ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    async def generate_tts_audio(self, text: str):
        import requests
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise Exception("ELEVENLABS_API_KEY no configurado")
        
        voice_id = "hpp4J3VqNfWAUOO0d1Us"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        text = self._preparar_texto_tts(text)
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.35, "similarity_boost": 0.8}
        }
        
        import asyncio
        loop = asyncio.get_event_loop()
        def fetch():
            return requests.post(url, headers=headers, json=data)
        response = await loop.run_in_executor(None, fetch)
        
        if response.status_code != 200:
            raise Exception(f"Error TTS: {response.text}")
        return response.content

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav"):
        import requests
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise Exception("ELEVENLABS_API_KEY no configurado")
            
        import mimetypes
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = "audio/wav"
            
        url = "https://api.elevenlabs.io/v1/speech-to-text"
        headers = {"xi-api-key": api_key}
        data = {"model_id": "scribe_v1"}
        files = {"file": (filename, audio_bytes, mime_type)}
        
        import asyncio
        loop = asyncio.get_event_loop()
        def fetch():
            return requests.post(url, headers=headers, data=data, files=files)
        response = await loop.run_in_executor(None, fetch)
            
        if response.status_code != 200:
            raise Exception(f"Error STT: {response.text}")
            
        return response.json().get("text", "")
