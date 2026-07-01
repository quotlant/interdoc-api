import chromadb #this is the vector database
from chromadb.utils import embedding_functions #this is the embedding function which will be used to convert text into vectors

client = chromadb.PersistentClient(path="./data/chroma_db") #this line creates a persistent client for the ChromaDB vector database, specifying the path where the database will be stored. persistent means that the data will be saved to disk and can be retrieved later, even after the program has stopped running.

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2") #this line initializes an embedding function using the SentenceTransformer model "all-MiniLM-L6-v2". This function will be used to convert text into vector representations for storage and retrieval in the vector database.

collection = client.get_or_create_collection(name="document", embedding_function=embedding_fn) #this line retrieves an existing collection named "document" from the ChromaDB database or creates a new one if it doesn't exist. The collection is associated with the specified embedding function, which will be used to generate vector embeddings for the text data stored in this collection. vector embeddings are numerical representations of text that capture semantic meaning, allowing for efficient similarity searches and retrieval of related documents based on their content.


def add_chunks(doc_id = str, chunks: list[str]): #this function takes a document ID and a list of text chunks as input and adds them to the ChromaDB collection. Each chunk is associated with the specified document ID, allowing for organized storage and retrieval of related text data.
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))] #this line generates unique IDs for each chunk by appending an index to the document ID. This ensures that each chunk can be individually identified and retrieved later.
    metadatas = [{"source": doc_id, "chunk_index": i} for i in range(len(chunks))] #this line creates a list of metadata dictionaries for each chunk, containing the source document ID and the index of the chunk. This metadata can be used for filtering and organizing the stored chunks in the database.
    collection.add(documents=chunks, ids=ids, metadatas=metadatas) #this line adds the chunks, their unique IDs, and associated metadata to the ChromaDB
    return len(chunks) #this line returns the number of chunks that were added to the collection, providing feedback on the operation's success.

def search_chunks(query: str, top_k: int = 4): #this function takes a query string and an optional parameter top_k (defaulting to 4) as input. It searches the ChromaDB collection for the most relevant chunks based on the query and returns the top_k results.
    return collection.query(query_texts=[query], n_results=top_k) #this line performs the search in the ChromaDB collection using the provided query string. It retrieves the top_k most relevant chunks based on their vector embeddings and returns the results, which can be used for further processing or display.