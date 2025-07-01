import streamlit as st
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
import pandas as pd
from merge_vcf import merge_vcf
from clean_vcf import clean_vcf, clean_clinvar
from langchain import hub



prompt = hub.pull("hwchase17/react")

tools = [merge_vcf, clean_vcf, clean_clinvar]
llm = ChatOllama(model='gemma3')

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

st.title('Genome Chat 2')
query = st.text_input('')
template = 'Answer in fewer than 100 words, do not use tools unless absolutely needed '

st.write(agent_executor.invoke({'input' : f'{template}{query}'}))
    

