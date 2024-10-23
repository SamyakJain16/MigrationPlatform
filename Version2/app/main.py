from .extract_pdf import extract_text_from_pdf
from .cv_analyzer import get_top_occupations_from_resume
from .retrieve_occupations import get_occupation_list
from .get_similarityscores import compute_similarity
from .get_best_occupations import find_max_per_row
from .preprocessor import remove_digits
from .get_results_schema import generate_occupation_data
from .get_results_openai import generate_new_results
from .llm_response_parser import parse_llm_response

from dotenv import load_dotenv
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from pinecone import Pinecone, ServerlessSpec
from typing import List
import logging
from io import BytesIO
from PyPDF2 import PdfReader
from bson import ObjectId
from .database import get_database
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Body
import openai
from openai import OpenAI
import os
from pydantic import BaseModel


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "pdf-index"

# Check if the index exists, if not create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embeddings are 1536 dimensions
        metric='cosine',
        spec=ServerlessSpec(
            cloud=os.getenv("PINECONE_CLOUD", "aws"),
            region=os.getenv("PINECONE_REGION", "us-east-1")
        )
    )
# Get the index
index = pc.Index(index_name)

client = OpenAI(api_key="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")
# -------------------------------------------------


@app.post("/query-pdf")
async def query_pdf(query: str = Body(...), pdf_id: str = Body(...), context: List[str] = Body([]), db=Depends(get_database)):
    try:
        # Retrieve PDF data
        pdf = await db.pdfs.find_one({"_id": ObjectId(pdf_id)})
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")

        # Create query embedding
        query_embedding = openai.embeddings.create(
            input=[query], model="text-embedding-ada-002")
        query_vector = query_embedding.data[0].embedding

        # Query Pinecone for the specific PDF
        results = index.query(vector=query_vector,
                              top_k=1, filter={"id": pdf_id})

        if results['matches']:
            relevant_text = results['matches'][0]['metadata']['text']
        else:
            # Fallback to stored text if no match in Pinecone
            relevant_text = pdf['text_content']

        # Construct prompt
        prompt = f"Based on the following context from a PDF document, please answer the question: {
            query}\n\nContext: {relevant_text}"

        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the content of PDF documents."},
                {"role": "user", "content": prompt}
            ]
        )

        return {"answer": response.choices[0].message.content}
    except Exception as e:
        print(f"Error querying PDF: {str(e)}")

# ------------------------------------------------
# PDF Endpoints


@app.post("/upload-pdf/{agent_id}")
async def upload_pdf(agent_id: str, file: UploadFile = File(...), db=Depends(get_database)):
    try:
        # Check the number of PDFs for this agent
        pdf_count = await db.pdfs.count_documents({"agent_id": agent_id})
        if pdf_count >= 5:
            raise HTTPException(
                status_code=400, detail="PDF upload limit reached")

        contents = await file.read()
        pdf = PdfReader(BytesIO(contents))
        num_pages = len(pdf.pages)

        # Extract text from PDF
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()

        # Create a unique ID for this PDF
        pdf_id = str(ObjectId())

        # Create embedding for the entire PDF content
        embeddings = openai.embeddings.create(
            input=[text_content], model="text-embedding-ada-002")
        vector = embeddings.data[0].embedding

        # Create a single record in Pinecone for this PDF
        index.upsert(vectors=[(pdf_id, vector, {"text": text_content})])

        pdf_data = {
            "_id": ObjectId(pdf_id),
            "agent_id": agent_id,
            "filename": file.filename,
            "content": contents,
            "pages": num_pages,
            "text_content": text_content  # Store the full extracted text
        }

        await db.pdfs.insert_one(pdf_data)

        print(f"PDF uploaded and indexed: {
              file.filename} for agent {agent_id}")
        return {"id": pdf_id, "filename": file.filename, "pages": num_pages}
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pdfs/{agent_id}")
async def list_pdfs(agent_id: str, db=Depends(get_database)):
    cursor = db.pdfs.find({"agent_id": agent_id}, {"content": 0})
    pdfs = await cursor.to_list(length=None)
    return [{"id": str(pdf["_id"]), "filename": pdf["filename"], "pages": pdf["pages"]} for pdf in pdfs]


@app.get("/pdfs/{agent_id}/{pdf_id}")
async def get_pdf(agent_id: str, pdf_id: str, db=Depends(get_database)):
    logger.info(f"Received request for PDF: agent_id={
                agent_id}, pdf_id={pdf_id}")
    try:
        pdf = await db.pdfs.find_one({"_id": ObjectId(pdf_id), "agent_id": agent_id})
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")

        content = pdf["content"]
        filename = pdf["filename"]

        # Ensure content is bytes
        if isinstance(content, str):
            content = content.encode('utf-8')
        elif isinstance(content, bytes):
            pass
        else:
            content = bytes(content)

        return StreamingResponse(
            BytesIO(content),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"Error retrieving PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/pdfs/{agent_id}/{pdf_id}")
async def delete_pdf(agent_id: str, pdf_id: str, db=Depends(get_database)):
    try:
        result = await db.pdfs.delete_one({"_id": ObjectId(pdf_id), "agent_id": agent_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="PDF not found")

        index.delete(ids=[pdf_id])

        return {"message": "PDF deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------------------
# Document Endpoints


@app.post("/documents/")
async def create_document(file: UploadFile = File(...), db=Depends(get_database)):
    try:
        contents = await file.read()
        print("File", file)
        document_data = {
            "filename": file.filename,
            "content": contents,
            "size": len(contents),
            "upload_date": datetime.now()
        }

        result = await db.documents.insert_one(document_data)

        return {
            "id": str(result.inserted_id),
            "filename": file.filename,
            "size": len(contents),
            "upload_date": document_data["upload_date"]
        }
    except Exception as e:
        print(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/")
async def list_documents(skip: int = 0, limit: int = 100, db=Depends(get_database)):
    cursor = db.documents.find({}, {"content": 0}).skip(skip).limit(limit)
    documents = await cursor.to_list(length=None)
    print(documents)
    return [
        {
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "size": doc["size"],
            "upload_date": doc["upload_date"]
        } for doc in documents
    ]


@app.get("/documents/{document_id}")
async def get_document(document_id: str, db=Depends(get_database)):
    try:
        document = await db.documents.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        content = document["content"]
        filename = document["filename"]

        return StreamingResponse(BytesIO(content), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail="Document not found")


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str, db=Depends(get_database)):
    try:
        result = await db.documents.delete_one({"_id": ObjectId(document_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/pdf/{agent_id}/{pdf_id}")
async def debug_pdf(agent_id: str, pdf_id: str, db=Depends(get_database)):
    pdf = await db.pdfs.find_one({"_id": ObjectId(pdf_id), "agent_id": agent_id})
    if pdf:
        return {
            "message": "PDF found",
            "filename": pdf["filename"],
            "agent_id": pdf["agent_id"],
            "id": str(pdf["_id"]),
            "content_length": len(pdf["content"])
        }
    else:
        return {"message": "PDF not found"}


# ----------------------------------------------------------------

# Import all the necessary functions from your Python files

class DocumentAnalysisRequest(BaseModel):
    document_id: str


def get_csv_path():
    # Get the directory of the current file (main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the CSV file
    csv_path = os.path.join(current_dir, 'occupation_list_main.csv')
    return csv_path


@app.post("/analyze-document")
async def analyze_document(request: DocumentAnalysisRequest, db=Depends(get_database)):
    try:
        document = await db.documents.find_one({"_id": ObjectId(request.document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Extract text from PDF
        pdf_content = BytesIO(document['content'])
        cv_resume_text = extract_text_from_pdf(pdf_content)
        print("PDF EXTR")
        # Get suggested occupations from CV text
        suggested_occupations = get_top_occupations_from_resume(cv_resume_text)

        csv_path = get_csv_path()
        # Retrieve occupation list from CSV
        occupation_lists = get_occupation_list(csv_path, 'Occupations')
        print("cwvvev")
        # Compute similarity scores
        similarity_results_df = compute_similarity(
            suggested_occupations, occupation_lists, model_name='all-mpnet-base-v2')

        # Find best occupations
        final_df = find_max_per_row(similarity_results_df)

        # Remove digits from final matched suggestions
        final_df['suggested_from_cv'] = final_df['suggested_from_cv'].apply(
            remove_digits)

        # Generate occupation data
        final_mapped_occupations = list(
            set(final_df['final_matched_suggestion'].to_list()))
        occupation_columns_dict, results = generate_occupation_data(
            csv_path, final_mapped_occupations)

        # Generate results using OpenAI or LLM
        result_openai = generate_new_results(occupation_columns_dict, results)
        print("resu open")
        # Parse LLM response
        final_result = parse_llm_response(result_openai)

        return {"analysis_result": final_result}
    except Exception as e:
        logging.error(f"Error in analyze_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
