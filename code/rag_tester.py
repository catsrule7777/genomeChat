from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings 
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

embedding_function = OllamaEmbeddings(model='nomic-embed-text:latest')
db = Chroma(persist_directory='./chroma_db', embedding_function=embedding_function)

retriever = db.as_retriever()

llm = ChatOllama(model='qwen3')

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)


chain = (
    {'context' : retriever, 'question' : RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke('What information is available?'))
