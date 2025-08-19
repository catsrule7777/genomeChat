from langchain.agents import tool 
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain_ollama import ChatOllama
import time
from langchain_anthropic import ChatAnthropic
import os

@tool(parse_docstring=True)
def fetch_from_vectorstore(question):
    """a tool that takes in a question, runs a similarity search using a paramater based on the question inside genome data vector store which has a row for each variant and columns such as chromosome, position, and Pathogenicity, and then returns the result"""
    
    metadata_field_info = [
        AttributeInfo(
            name='source',
            description='The source of the information. This is most likely merged.csv',
            type='string',
        ),
        AttributeInfo(
            name='row',
            description='The row the variant is on in the merged.csv file.',
            type='string',
        ),
        AttributeInfo(
            name='chromosome',
            description='The chromosome the variant is located in.',
            type='string',
        ),
        AttributeInfo(
            name='position',
            description='The position the variant is located in on its chromosome.',
            type='string',
        ),
        AttributeInfo(
            name='clinical_significance',
            description='The clinical significance of the variant. Likely one of [Benign, Pathogenic, Uncertain_significance, Likely_pathogenic, Likely_benign, not_provided, Conflicting_classifications_of_pathogenicity, Benign/Likely_benign, drug_response, association]',
            type='string'
        ),
        AttributeInfo(
            name='clnhgvs',
            description='HGVS variant ID',
            type='string'
        ),
        AttributeInfo(
            name='clndn',
            description='Diseases related to the variant.',
            type='string'
        ),
        AttributeInfo(
            name='gene',
            description='name of the gene variant is on',
            type='string'
        ),
    ]

    document_content_description = 'Information about a certain variant, including clinical significance, chromosome, and position on that chromosome.'

    print("Starting tool code (fetch_from_vectorstore) ...")
    import chromadb 
    from langchain_ollama import OllamaEmbeddings 
    from langchain_chroma import Chroma
    print('finished imports')
    #client = chromadb.PersistentClient(path='./chroma_db')
    #col = client.list_collections()
    api_key = os.getenv('ANTHROPIC_API_KEY')

    #col1 = client.get_collection('langchain')
    #llm = ChatOllama(model='qwen3:latest', num_ctx=8192)
    llm = ChatAnthropic(model='claude-sonnet-4-20250514')

    embeddings = OllamaEmbeddings(model='nomic-embed-text:latest')

    print("finished loading embeddings")

    vector_store = Chroma(
        collection_name = 'langchain',
        embedding_function = embeddings,
        persist_directory='./chroma_db'
    )

    
    print("question = "+question)
    #print(vector_store.similarity_search(params))
    #return vector_store.similarity_search(params)
    # retriever = vector_store.as_retriever(search_kwargs={'k':500})
    #retriever = vector_store.as_retriever(search_kwargs={'k':50})
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vector_store,
        document_content_description,
        metadata_field_info,
        search_kwargs={'k':350}
    )
    start_time = time.time()
    x = retriever.invoke(question)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Similarity Search finished in {elapsed_time:.4f} seconds')
    return x






