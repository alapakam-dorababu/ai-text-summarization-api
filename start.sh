#!/bin/bash

echo "🚀 Starting Ollama server..."

# Start Ollama in the background
ollama serve &

# Wait until Ollama is ready
until ollama list >/dev/null 2>&1; do
  echo "⏳ Waiting for Ollama to start..."
  sleep 2
done

echo "✅ Ollama server is started and running!"

# Pull the required model
echo "📥 Downloading model: mistral..."
ollama pull mistral

echo "🎯 Model 'mistral' is downloaded and ready!"

# Start FastAPI
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
