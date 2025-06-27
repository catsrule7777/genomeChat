import streamlit as st
from langchain_ollama import ChatOllama
from clean_vcf import clean_vcf
from langchain.agents import initialize_agent, AgentType, create_tool_calling_agent, AgentExecutor, tool, create_react_agent
from langchain.agents import Tool
from clean_vcf import clean_clinvar
from merge_vcf import merge_vcf
from langchain_core.prompts import ChatPromptTemplate
#from langchain_core.tools import tool
import pandas as pd
from langchain_core.prompts import PromptTemplate

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''


prompt = PromptTemplate.from_template(template)

@tool
def merge_vcf(paths):
    """a tool that takes in two comma seperated file paths, and returns the merged result of the two files"""
    paths = paths.split(',')
    vcf_path = paths[0].strip(' ')
    clinvar_path = paths[1].strip(' ')
    vcf = pd.read_csv(vcf_path)
    clinvar = pd.read_csv(clinvar_path)

    vcf['CHROM'] = vcf['CHROM'].str.strip('chr')
    vcf['CHROM'] = vcf['CHROM'].astype(int)
    vcf['POS'] = vcf['POS'].astype(int)
    merged = vcf.merge(clinvar, on=['CHROM', 'POS'], how='inner')

    merged.to_csv('merged.csv')

    return merged

@tool 
def combine_strings(string:str) -> str:
    """a tool that takes in a string, and outputs a string"""
    lst = string.split(',')
    str1 = lst[0]
    str2 = lst[1]
    return str(str1) + str(str2)

@tool 
def addTwoNumbers(nums: str) -> float:
    """takes in two comma seperate numbers, and adds them"""
    nums = nums.split(',')
    num1 = int(nums[0])
    num2 = int(nums[1])
    return num1 + num2


llm = ChatOllama(model='gemma3')

def calculate(expression):
    return str(eval(expression))



vcf_cleaning_tool = Tool(name='vcf cleaner (not clinvar)', func=clean_vcf, description='A tool that takes in a users vcf and then cleans the vcf by extracting useful informatoin and storing it in a csv file - does NOT work with clivnar')
calculate_tool = Tool(name='calculator', func=calculate, description='A tool that takes in an expression (as a string) and returns a str ex: 2 + 2 -> 4')
clinvar_cleaning_tool = Tool(name='clinvar vcf cleaner', func=clean_clinvar, description='A tool that takes in a clinvar vcf and extracts useful informatoin, and then downloads the new df as a csv')

tools = [addTwoNumbers, vcf_cleaning_tool, clinvar_cleaning_tool, merge_vcf, combine_strings]
#tools = [vcf_cleaning_tool]
#tools = [calculate_tool, vcf_cleaning_tool, clinvar_cleaning_tool, merge_vcf]
#tools = [merge_vcf]

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

st.title('Genome Chat')
query = st.text_input('')
template = 'Answer in fewer than 100 words: '
#response = llm.invoke(f'{template}{query}')
#print(response.content)
result = agent_executor.invoke({'input' : f'{template}{query}'})

#st.write(response.content)
st.write(result)