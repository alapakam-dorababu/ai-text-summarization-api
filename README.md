# AI-Powered Text Summarization API

## Overview
The AI-Powered Text Summarization API provides concise summaries of text input using advanced language models. Built with FastAPI, it integrates Ollama (LLMs) and LangChain for enhanced language processing. The API supports multiple input formats, including raw text, URLs, and PDFs. It includes authentication, caching, and efficient request handling for a seamless user experience.

## Features
- Accepts text input and returns a summarized version.
- Supports multiple languages for summarization.
- Extracts and summarizes text from:
  - Raw text
  - Web URLs
  - PDF documents
- Asynchronous request handling for fast processing.
- Caches recent summaries using Redis for improved performance.
- Implements JWT authentication for secure API access.
- Rate limiting to prevent abuse.
- Logs and monitors API usage.

## Technology Stack
- **Backend**: FastAPI (Python)
- **LLMs**: Ollama (Large Language Models)
- **Database**: SQLite (for development) / PostgreSQL (for production)
- **Cache**: Redis
- **Authentication**: JWT (JSON Web Token)
- **Containerization**: Docker Compose

## System Architecture
### High-Level Flow
1. **User Authentication**: Clients authenticate using JWT.
2. **Text Submission**: Users submit raw text, a URL, or a PDF.
3. **Preprocessing**:
   - If a URL is provided, the system fetches and extracts text.
   - If a PDF is provided, the system extracts readable text.
4. **Summarization**: The extracted text is processed using Ollama LLM via LangChain.
5. **Caching**: Recent summaries are stored in Redis for quick retrieval.
6. **Response**: The summarized text is returned to the user.

## API Endpoints
### Authentication
- `POST /auth/login` – Authenticate user and return JWT token.
- `POST /auth/register` – Register a new user.

### Summarization
- `POST /summarize/text` – Summarize a given text input.
  - **Input**: JSON body containing text.
  - **Output**: Summarized version of the text.
- `POST /summarize/url` – Summarize text extracted from a URL.
  - **Input**: JSON body containing a URL.
  - **Output**: Summarized version of the extracted content.
- `POST /summarize/pdf` – Summarize text extracted from an uploaded PDF.
  - **Input**: PDF file.
  - **Output**: Summarized version of the extracted text.

### Caching & Logs
- `GET /cache/recent` – Retrieve recently summarized texts from Redis.
- `GET /logs/usage` – Get API usage logs.

## Security & Rate Limiting
- Implements JWT authentication for secure access.
- Applies rate limiting to prevent excessive API requests.
- Uses CORS policies to control access.
- Encrypts stored data and API keys where applicable.

## Getting Started
### Prerequisites
- Python 3.10+
- FastAPI
- Redis
- PostgreSQL (for production)
- Docker & Docker Compose

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/alapakam-dorababu/ai-text-summarization-api.git
   cd ai-text-summarization-api
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```sh
   cp .env.example .env
   ```

### Running with Docker Compose
1. Build and start the services:
   ```sh
   docker-compose up --build -d
   ```
2. Stop the services:
   ```sh
   docker-compose down
   ```

### Database Migrations

See the full Alembic setup guide in [Database Migrations with Alembic ](migrations/README.md).


## Usage
After starting the API, you can test it using:
```sh
curl -X POST "http://localhost:8000/summarize/text" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{"text": "Your long text here..."}'
```

## License
This project is licensed under the MIT License.

---

Feel free to update this `README.md` with your repository URL and any additional details specific to your deployment setup!
