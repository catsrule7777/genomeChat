from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings 
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

embeddings = OllamaEmbeddings(model='nomic-embed-text:latest')

vectordb = Chroma(persist_directory='./chromadb', embedding_function=embeddings)

retriever = vectordb.as_retriever()





template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOllama(model='qwen3')

chain = (
    {'context' : retriever, 'question' : RunnablePassthrough()}
    | prompt
    | model 
    | StrOutputParser()
)

print(chain.invoke('What is some information about the file?'))
