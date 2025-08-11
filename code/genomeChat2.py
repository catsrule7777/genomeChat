import streamlit as st
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
import pandas as pd
from merge_vcf import merge_vcf
from clean_vcf import clean_vcf, clean_clinvar
from langchain import hub
from dotenv import load_dotenv
import os 
from langchain_openai import ChatOpenAI 
from chromatest import fetch_from_vectorstore

print("Starting...")

load_dotenv()
api_key = os.getenv('OPENAI_KEY')

prompt = hub.pull("hwchase17/react")

print("React prompt = "+str(prompt))

#tools = [merge_vcf, clean_vcf, clean_clinvar]
print("Loading tools...")
tools = [fetch_from_vectorstore]

print("Starting ChatOllama...")
llm = ChatOllama(model='qwen3:latest', num_ctx=8192)

print("Creating react agent...")
agent = create_react_agent(llm, tools, prompt)

print("Creating AgentExecutor...")
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)



st.title('Genome Chat 2')

with st.form('form'):
    query = st.text_input('')
    template = 'Answer in fewer than 500 words, use fetch_from_vectorstore tool for looking up info about personal genome variants and for counting those variants, do not think for too long, have at most 200 words of thinking'

    submit_button = st.form_submit_button('Submit')

    if submit_button:
        
        print("Calling agent_executor invoke...")
        st.write(agent_executor.invoke({'input' : f'{template}\n{query}'}))
        
        print("Completed agent_executor invoke...")
    

