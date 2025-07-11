from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.processing.embedder import embeddings

def load_qa_chain():
    embeddings = OpenAIEmbeddings(
    model=os.getenv("AZURE_MODEL"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_EMBEDDING_KEY"),
    default_query={"api-version":"preview"}
    )
    index = FAISS.load_local("data/faiss_index", embeddings,allow_dangerous_deserialization=True)
    llm = ChatOpenAI(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        default_query={"api-version":"preview"}
    )
    parser= StrOutputParser()
    prompt = PromptTemplate.from_template(
    """You are a helpful assistant. Based only on the product data below, answer the user's question accurately.

    Data:
    {context}

    Question: {input}
    Answer:"""
 )
    qa = create_stuff_documents_chain(llm,prompt,output_parser=parser)
    ans= create_retrieval_chain(index.as_retriever(),qa)
    return ans

def ask_question(query):
    qa = load_qa_chain()
    result = qa.invoke({"input": query})
    return result["answer"]

print(ask_question("who are the characters in the story?"))