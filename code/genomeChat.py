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

#Question: the input question you must answer

template_PT = '''You are a helpful assistant with access to tools.  Answer the user's questions by using tools when needed.

Get a final response quickly, in under 4 thoughts.
You have access to the following tools:
{tools}

Use the following format:

Thought: think
Action: the action to take, using these tools is optional: [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat 3 times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

template_CPT = "Answer this query using {tools} if they are useful"

prompt = PromptTemplate.from_template(template_PT)

@tool
def merge_vcf(vcf_path, clinvar_path):
    """a tool that takes in two file paths, and returns the merged result of the two files"""
    vcf = pd.read_csv(vcf_path)
    clinvar = pd.read_csv(clinvar_path)

    vcf['CHROM'] = vcf['CHROM'].str.strip('chr')
    vcf['CHROM'] = vcf['CHROM'].astype(int)
    vcf['POS'] = vcf['POS'].astype(int)
    merged = vcf.merge(clinvar, on=['CHROM', 'POS'], how='inner')

    merged.to_csv('merged.csv')

    return merged

@tool 
def combine_strings(str1: str, str2: str) -> str:
    """a tool that takes in two strings, and outputs a combined string
    Args:
        str1: The first string
        str2: The second string
    """

    #lst = string.split(',')
    return "The combined strings: " + str(str1) + str(str2)

@tool 
def addTwoNumbers(nums: str) -> float:
    """takes in two comma seperate numbers, and adds them"""
    nums = nums.split(',')
    num1 = int(nums[0])
    num2 = int(nums[1])
    return num1 + num2


llm = ChatOllama(model='llama3.2')

def calculate(expression):
    return str(eval(expression))



vcf_cleaning_tool = Tool(name='vcf cleaner (not clinvar)', func=clean_vcf, description='A tool that takes in a users vcf and then cleans the vcf by extracting useful informatoin and storing it in a csv file - does NOT work with clivnar')
calculate_tool = Tool(name='calculator', func=calculate, description='A tool that takes in an expression (as a string) and returns a str ex: 2 + 2 -> 4')
clinvar_cleaning_tool = Tool(name='clinvar vcf cleaner', func=clean_clinvar, description='A tool that takes in a clinvar vcf and extracts useful informatoin, and then downloads the new df as a csv')

tools = [combine_strings]
#tools = [addTwoNumbers, combine_strings, vcf_cleaning_tool, clinvar_cleaning_tool, merge_vcf]
#tools = [vcf_cleaning_tool]
#tools = [calculate_tool, vcf_cleaning_tool, clinvar_cleaning_tool, merge_vcf]
#tools = [merge_vcf]

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

st.title('Genome Chat')
query = st.text_input('')
template = 'Answer in fewer than 100 words, and only use tools when needed: '
#response = llm.invoke(f'{template}{query}')
#print(response.content)
file = st.file_uploader('Upload a file')
if file:
    file_contents = file.read()

if file:
    result = agent_executor.invoke({'input' : f'{template}{query}{file_contents}'})
    st.write(result['output'])
    #print("file results = "+result)
else:
    result = agent_executor.invoke({'input' : f'{template}{query}'})
    st.write(result['output'])
    #print("non-file results = "+result)

#st.write(result)
#st.write(response.content)
