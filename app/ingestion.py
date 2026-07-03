import io
from pypdf import PdfReader

def extract_text(filename: str, file_bytes: bytes) -> str: #this function takes a filename and file bytes as input and returns the extracted text from the PDF file. file byte is the content of the pdf in bytes format
    if filename.lower().endswith('.pdf'):
        reader = PdfReader(io.BytesIO(file_bytes)) #this line creates a PdfReader object from the file bytes using io.BytesIO to read the bytes as a file-like object
        return "\n".join(page.extract_text() for page in reader.pages) #this line extracts the text from each page of the PDF and joins them with newline characters to return a single string containing all the extracted text
    return file_bytes.decode('utf-8', errors='ignore') #if the file is not a PDF, it decodes the file bytes as a UTF-8 string and ignores any errors that may occur during decoding

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]: #this function takes a string of text and splits it into smaller chunks of a specified size with a specified overlap between chunks. It returns a list of strings, where each string is a chunk of the original text.
    words = text.split() #this line splits the input text into a list of words using whitespace as the delimiter
    chunks = [] #this line initializes an empty list to store the resulting chunks of text
    start = 0 #this line initializes a variable to keep track of the starting index for each chunk
    while start < len(words): #this line starts a loop that continues until the starting index reaches the end of the list of words
        end = start + chunk_size #this line calculates the ending index for the current chunk by adding the chunk size to the starting index
        chunk = " ".join(words[start:end]) #this line creates a chunk of text by
        if chunk.strip(): #this line checks if the chunk is not empty after stripping whitespace
            chunks.append(chunk) #this line adds the non-empty chunk to the list of chunks
        start += chunk_size - overlap #this line updates the starting index for the next chunk by moving it forward by the chunk size minus the overlap, allowing for overlapping chunks
    return chunks #this line returns the list of chunks created from the original textgit ß
