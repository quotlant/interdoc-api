from fastapi import FastAPI, UploadFile, File
from app.ingestion import extract_text, chunk_text
from app.vectorspace import add_chunks

app = FastAPI(title='Document Intelligence API', 
              description='An API for document ingestion and vector storage', 
              version='1.0.0')

@app.get("/") #this line defines a GET endpoint at the root URL ("/") of the API. When accessed, it will return a simple JSON response indicating that the API is running.
def root():
    return {"status": "alive"} #this line returns a JSON response with a key "status" and value "alive", indicating that the API is operational.

@app.post("/upload") #this line defines a POST endpoint at the URL "/upload/" of the API. It is designed to handle file uploads, allowing users to send files to the server for processing.
async def upload_file(file: UploadFile = File(...)): #this line defines an asynchronous function named upload_file that takes a single parameter file of type UploadFile. The File(...) indicates that this parameter is required and will be provided as part of the request body when a user uploads a file. asynchronous functions allow for non-blocking operations, which is useful for handling file uploads and other I/O-bound tasks.
    contents = await file.read()
    text = extract_text(file.filename, contents)
    chunks = chunk_text(text) #this line calls the chunk_text function, passing the extracted text as an argument. The function splits the text into smaller chunks based on the specified chunk size and overlap, returning a list of text chunks.
    n = add_chunks(doc_id = file.filename, chunks=chunks) #this line calls the add_chunks function, passing the filename as the document ID and the list of text chunks. The function adds the chunks to the ChromaDB collection, associating them with the specified document ID. It returns the number of chunks that were successfully added to the collection.
    return {"filename": file.filename, "chunks_created": n} #this line returns a JSON response containing the original filename and the number of chunks created from the uploaded file. This provides feedback to the user about the result of the upload and processing operation.