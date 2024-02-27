from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.voyageai import VoyageEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_pinecone import Pinecone
from dotenv import load_dotenv
from app.config import SOURCES_PER_QUESTION
from os import getenv

load_dotenv()

PINECONE_API_KEY = getenv("PINECONE_API_KEY")
VOYAGE_API_KEY = getenv("VOYAGE_API_KEY")
NAMESPACE = getenv("NAMESPACE")
INDEX_NAME = getenv("INDEX_NAME")

embeddings = VoyageEmbeddings(model="voyage-2", voyage_api_key=VOYAGE_API_KEY)
vectorstore = Pinecone(
    index_name=INDEX_NAME,
    embedding=embeddings,
    pinecone_api_key=PINECONE_API_KEY,
    namespace=NAMESPACE,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": SOURCES_PER_QUESTION})

# --------------- BASE LLMs -----------------
llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    verbose=False,
    request_timeout=240,
    temperature=0.5,
    streaming=True,
)
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(), llm=llm
)

# -------------- MEMORIES -------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# -------------- CHAINS ---------------
QA_chain = RetrievalQAWithSourcesChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
)
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm, retriever=multi_retriever, return_source_documents=True, verbose=True
)
