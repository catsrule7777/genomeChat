from langchain.agents import tool 

@tool(parse_docstring=True)
def fetch_from_vectorstore(params):
    """a tool that takes in a search string, runs a similarity search inside genome data vector store which has a row for each variant and columns such as chromosome, position, and Pathogenicity, and then returns the result"""
    
    print("Starting tool code (fetch_from_vectorstore) ...")
    import chromadb 
    from langchain_ollama import OllamaEmbeddings 
    from langchain_chroma import Chroma
    print('finished imports')
    #client = chromadb.PersistentClient(path='./chroma_db')
    #col = client.list_collections()

    #col1 = client.get_collection('langchain')


    embeddings = OllamaEmbeddings(model='nomic-embed-text:latest')

    print("finished loading embeddings")

    vector_store = Chroma(
        collection_name = 'langchain',
        embedding_function = embeddings,
        persist_directory='./chromadb'
    )

    
    print("params = "+params)
    #print(vector_store.similarity_search(params))
    #return vector_store.similarity_search(params)
    # retriever = vector_store.as_retriever(search_kwargs={'k':500})
    retriever = vector_store.as_retriever(search_kwargs={'k':20})
    #print(retriever.invoke(params))
    print('similarity search done')
    return retriever.invoke(params)






