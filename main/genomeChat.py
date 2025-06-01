import streamlit as st
from langchain_ollama import ChatOllama


llm = ChatOllama(model='gemma3')

st.title('Genome Chat')
query = st.text_input('')
template = 'Answer in fewer than 200 words: '
response = llm.invoke(f'{template}{query}')
print(response.content)
st.write(response.content)