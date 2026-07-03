from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.ingestion import extract_text, chunk_text
from app.vectorspace import add_chunks, search_chunks
from app.rag import generate_answer 
from fastapi.middleware.cors import CORSMiddleware #this is a security feature implemented by web browsers that restricts web pages from making requests to a different domain than the one that served the web page. 


app = FastAPI(title='Document Intelligence API', 
              description='An API for document ingestion and vector storage', 
              version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel): #this line defines a Pydantic model named QueryRequest, which is used to validate and parse incoming request data for the query endpoint. Pydantic models are used in FastAPI to define the expected structure of request bodies, ensuring that the data received matches the specified format.
    question: str
    top_k: int = 4
    
    

@app.get("/health") #this line defines a GET endpoint at the root URL ("/") of the API. When accessed, it will return a simple JSON response indicating that the API is running.
def root():
    return {"status": "alive"} #this line returns a JSON response with a key "status" and value "alive", indicating that the API is operational.

@app.post("/upload") #this line defines a POST endpoint at the URL "/upload/" of the API. It is designed to handle file uploads, allowing users to send files to the server for processing.
async def upload_file(file: UploadFile = File(...)): #this line defines an asynchronous function named upload_file that takes a single parameter file of type UploadFile. The File(...) indicates that this parameter is required and will be provided as part of the request body when a user uploads a file. asynchronous functions allow for non-blocking operations, which is useful for handling file uploads and other I/O-bound tasks.
    contents = await file.read() 
    text = extract_text(file.filename, contents) #this line calls the extract_text function, passing the filename and the contents of the uploaded file as arguments. The function extracts the text from the file (e.g., PDF or plain text) and returns it as a string, which is then stored in the variable text.
    chunks = chunk_text(text) #this line calls the chunk_text function, passing the extracted text as an argument. The function splits the text into smaller chunks based on the specified chunk size and overlap, returning a list of text chunks.
    n = add_chunks(doc_id = file.filename, chunks=chunks) #this line calls the add_chunks function, passing the filename as the document ID and the list of text chunks. The function adds the chunks to the ChromaDB collection, associating them with the specified document ID. It returns the number of chunks that were successfully added to the collection.
    return {"filename": file.filename, "chunks_created": n} #this line returns a JSON response containing the original filename and the number of chunks created from the uploaded file. This provides feedback to the user about the result of the upload and processing operation.


@app.post("/query") #this line defines a POST endpoint at the URL "/query/" of the API. It is designed to handle queries, allowing users to send questions to the server for processing and retrieval of relevant information from the stored documents.
async def query_documents(request: QueryRequest): #this line defines an asynchronous function named query_documents that takes a single parameter request of type QueryRequest. The QueryRequest class is expected to contain a question attribute, which will be used to perform the search and generate an answer. 
    results = search_chunks(request.question, top_k=request.top_k) #this line calls the search_chunks function, passing the question from the request and the top_k value. The function searches the ChromaDB collection for the most relevant chunks based on the query and returns the results.
    return generate_answer(request.question, results) #this line calls the generate_answer function, passing the question and the search results. The function generates an answer based on the retrieved chunks and returns it as a JSON response, which includes the answer text and the sources used to generate that answer.

