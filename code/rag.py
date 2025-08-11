from langchain_community.document_loaders import CSVLoader
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding_function = OllamaEmbeddings(model='nomic-embed-text:latest')

loader = CSVLoader('merged.csv')
documents = loader.load()

#text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
#documents_split = text_splitter.split_documents(documents)

#db = Chroma.from_documents(documents_split, embedding_function, persist_directory='')

db = Chroma.from_documents(documents, embedding_function, persist_directory='./chroma_db')

retriever = db.as_retriever()





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


