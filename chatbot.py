import os
import dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

dotenv.load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')


class AdjustedHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def __call__(self, input):
        return super().__call__(input)


def create_chain(chains, pdf_doc, use_local_model=True):
    if pdf_doc is None:
        return 'You must convert or upload a pdf first'
    db = create_vector_db(pdf_doc)
    llm = create_model(use_local_model)
    prompt_search_query = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(
            variable_name="chat_history"),
        ("user", "{input}"),
        ("user",
         "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
    ])
    retriever_chain = create_history_aware_retriever(llm, db.as_retriever(), prompt_search_query)
    prompt_get_answer = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\\n\\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_get_answer)
    chains[0] = create_retrieval_chain(retriever_chain, combine_docs_chain)
    return 'Document has successfully been loaded'


def create_model(local: bool):
    if local:
        llm = Ollama(model='phi')
    else:
        llm = HuggingFaceEndpoint(
            repo_id="OpenAssistant/oasst-sft-1-pythia-12b",
            model_kwargs={"max_length": 256},
            temperature=1.0
        )
    return llm


def create_vector_db(doc):
    document = load_document(doc)
    text = split_document(document)
    embedding = AdjustedHuggingFaceEmbeddings()
    db = Chroma.from_documents(text, embedding)
    return db


def load_document(doc):
    loader = PyMuPDFLoader(doc.name)
    document = loader.load()
    return document


def split_document(doc):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text = text_splitter.split_documents(doc)
    return text


def save_history(history):
    with open('history.txt', 'w') as file:
        for s in history:
            file.write(f'- {s.content}\n')


def answer_query(chain, query: str, chat_history=None) -> str:
    if chain:
        # run the given chain with the given query and history
        chat_history.append(HumanMessage(content=query))
        response = chain.invoke({
            'chat_history': chat_history,
            'input': query
        })
        answer = response['answer']
        print('RESPONSE: ', answer, '\n\n')
        # add the current question and answer to history
        chat_history.append(AIMessage(content=answer))
        # save chat history to text file
        save_history(chat_history)
        return answer
    else:
        return "Please load a document first."
