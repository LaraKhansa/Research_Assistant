import os
import dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.api import client as chromadb_client
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder


dotenv.load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')


class AdjustedHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def __call__(self, input):
        return super().__call__(input)


class ConversationalRAGModel():
    def __init__(self, use_local_model: bool = True):
        self.llm = create_model(use_local_model)
        self.retrieval_chain = None
        # chat history to be passed to the model along with every query
        self.chat_history = None

    def create_chain(self, docs: list) -> None:
        """
        This method creates the essential conversational_rag_chain attribute which can
        be used later to answer queries within a conversation based on the given documents
        """
        # clear cache if it exists
        if hasattr(self, 'db') and self.db:
            chromadb_client.SharedSystemClient.clear_system_cache()
        self.db = create_vector_db(docs)
        prompt_search_query = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(
            variable_name="chat_history"),
            ("user", "{input}"),
            ("user",
            "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
        ])
        retriever_chain = create_history_aware_retriever(self.llm, self.db.as_retriever(), prompt_search_query)
        prompt_get_answer = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's question clearly and concisely using the following context:\\n\\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        combine_docs_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt_get_answer)
        # basically combine 2 chains into 1 chain
        self.retrieval_chain = create_retrieval_chain(retriever_chain, combine_docs_chain)
        # initiate chat history attribute
        self.chat_history = []

    def answer(self, query: str) -> str:
        if not self.retrieval_chain:
            return 'Please load files first'
        # update the chat history with the given query
        self.chat_history.append(HumanMessage(content=query))
        response = self.retrieval_chain.invoke({
            'chat_history': self.chat_history,
            'input': query
        })
        answer = response['answer']
        self.chat_history.append(AIMessage(content=answer))
        return answer

    def reset(self) -> None:
        """
        Resets the chat history & model to None
        """
        self.retrieval_chain = None
        self.chat_history = None


def create_model(local: bool):
    if local:
        llm = Ollama(model='phi')
    else:
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            model_kwargs={"max_length": 256},
            temperature=1.0
        )
    return llm


def create_vector_db(docs: list) -> Chroma:
    """
    Creates a vector database from a list of documents.
    """
    # divide documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text = []
    for doc in docs:
        text.extend(text_splitter.split_documents(load_document(doc)))
    # create embedding function
    embedding = HuggingFaceEmbeddings()
    db = Chroma.from_documents(text, embedding)
    return db


def load_document(doc):
    print(doc)
    if doc.endswith('.md') or doc.endswith('.txt'):
        loader = TextLoader(doc, encoding='utf-8')
    else:
        loader = PyMuPDFLoader(doc.name)
    return loader.load()


def save_history(history):
    with open('history.txt', 'w') as file:
        for s in history:
            file.write(f'- {s.content}\n')
