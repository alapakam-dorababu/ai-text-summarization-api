import pypdf
import docx
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException, UploadFile


def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        pdf_reader = pypdf.PdfReader(file.file)
        return "\n".join(
            [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


def extract_text_from_docx(file: UploadFile) -> str:
    try:
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing DOCX: {str(e)}")


def extract_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch webpage")
        soup = BeautifulSoup(response.text, "html.parser")
        return " ".join([p.get_text() for p in soup.find_all("p")])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")
