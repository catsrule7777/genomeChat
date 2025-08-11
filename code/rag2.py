from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings 
from langchain_community.document_loaders import CSVLoader
from langchain.schema import Document
import pandas as pd


df = pd.read_csv('merged.csv')

embedding_function = OllamaEmbeddings(model='nomic-embed-text:latest')
#loader = CSVLoader('merged.csv')
#documents = loader.load()

documents = []

for idx in df.index:
    chrom = df.loc[idx, 'CHROM']
    pos = df.loc[idx, 'POS']
    ref_x = df.loc[idx, 'REF_x']
    alt_x = df.loc[idx, 'ALT_x']
    ref_y = df.loc[idx, 'REF_y']
    alt_y = df.loc[idx, 'ALT_y']
    clnsig = df.loc[idx, 'CLNSIG_y']

    page_content = f'Variant at chromosome {chrom}, position {pos}. It has {clnsig} clinical significance.'
    metadata = {'source':'merged.csv', 'row':str(idx), 'chromosome':str(chrom), 'position':str(pos), 'clinical_significance':str(clnsig)}   
    document = Document(page_content=page_content, metadata=metadata)
    documents.append(document)
    print(document)

db = Chroma.from_documents(
    documents=documents,
    embedding=embedding_function,
    persist_directory='./chromadb'
)





'''
db = Chroma(
    collection_name='collection1',
    embedding_function=embedding_function,
    persist_directory='./chromadb'
)

ids = ['1']
db.add_documents(documents=documents, ids=ids)
'''