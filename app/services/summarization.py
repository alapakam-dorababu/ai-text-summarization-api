import ollama
from fastapi import HTTPException
from app.core.config import OLLAMA_MODEL
from app.utils.extractors import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_url,
)


def summarize_text(text: str) -> str:
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}],
        )
        return response.get("message", {}).get("content", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Ollama: {str(e)}")


def summarize_pdf(file):
    text = extract_text_from_pdf(file)
    return summarize_text(text)


def summarize_docx(file):
    text = extract_text_from_docx(file)
    return summarize_text(text)


def summarize_url(url: str):
    text = extract_text_from_url(url)
    return summarize_text(text)
