#!/bin/bash

echo "🏭 Lean AI Assistant - Quick Start"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
    read -p "Press Enter after adding your API keys to .env..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🚀 Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check backend health
echo "🔍 Checking backend health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend is not ready yet, wait a moment..."
fi

echo ""
echo "=================================="
echo "✅ Lean AI Assistant is running!"
echo "=================================="
echo ""
echo "📍 Access points:"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Frontend:     http://localhost:8501"
echo "   Qdrant UI:    http://localhost:6333/dashboard"
echo ""
echo "📚 Next steps:"
echo "   1. Add PDF files to backend/data/knowledge_base/"
echo "   2. Run: python scripts/ingest_documents.py"
echo "   3. Open frontend and start chatting!"
echo ""
echo "🛑 To stop: docker-compose down"
echo ""
