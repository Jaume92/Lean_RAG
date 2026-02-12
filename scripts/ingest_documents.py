#!/usr/bin/env python3
"""
Script para ingerir documentos PDF a la base de conocimientos Qdrant
"""

import os
import sys
from pathlib import Path
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from tqdm import tqdm
import hashlib

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "lean_knowledge")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from PDF file
    """
    reader = PdfReader(pdf_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    
    return text

def process_document(
    file_path: Path, 
    embeddings_model: SentenceTransformer,
    client: QdrantClient
) -> int:
    """
    Process a single document and add to Qdrant
    
    Returns:
        Number of chunks added
    """
    print(f"Processing: {file_path.name}")
    
    # Extract text
    if file_path.suffix.lower() == '.pdf':
        text = extract_text_from_pdf(file_path)
    else:
        print(f"Unsupported file type: {file_path.suffix}")
        return 0
    
    # Chunk text
    chunks = chunk_text(text)
    
    # Create embeddings and points
    points = []
    for i, chunk in enumerate(tqdm(chunks, desc="Creating embeddings")):
        # Generate embedding
        embedding = embeddings_model.encode(chunk).tolist()
        
        # Create unique ID
        chunk_id = hashlib.md5(f"{file_path.name}_{i}".encode()).hexdigest()
        
        # Create point
        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": chunk,
                "source": file_path.name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
        )
        points.append(point)
    
    # Upload to Qdrant in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
    
    print(f"✅ Added {len(chunks)} chunks from {file_path.name}")
    return len(chunks)

def setup_collection(client: QdrantClient, vector_size: int):
    """
    Create Qdrant collection if it doesn't exist
    """
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    if COLLECTION_NAME not in collection_names:
        print(f"Creating collection: {COLLECTION_NAME}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
        print("✅ Collection created")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists")

def main():
    """
    Main ingestion function
    """
    print("🏭 Lean AI Assistant - Document Ingestion")
    print("=" * 50)
    
    # Initialize Qdrant client
    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    # Initialize embeddings model
    print(f"Loading embeddings model: {EMBEDDING_MODEL}...")
    embeddings_model = SentenceTransformer(EMBEDDING_MODEL)
    vector_size = embeddings_model.get_sentence_embedding_dimension()
    
    # Setup collection
    setup_collection(client, vector_size)
    
    # Get documents directory
    data_dir = Path(__file__).parent.parent / "backend" / "data" / "knowledge_base"
    
    if not data_dir.exists():
        print(f"❌ Directory not found: {data_dir}")
        sys.exit(1)
    
    # Find all PDF files
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {data_dir}")
        print("\nPor favor, añade archivos PDF a backend/data/knowledge_base/")
        print("\nLibros recomendados:")
        print("  - Toyota Production System (Taiichi Ohno)")
        print("  - Lean Thinking (Womack & Jones)")
        print("  - The Machine That Changed the World")
        print("  - Learning to See (Mike Rother)")
        sys.exit(1)
    
    print(f"\nFound {len(pdf_files)} PDF files")
    print("-" * 50)
    
    # Process each document
    total_chunks = 0
    for pdf_file in pdf_files:
        chunks = process_document(pdf_file, embeddings_model, client)
        total_chunks += chunks
        print()
    
    print("=" * 50)
    print(f"✅ Ingestion complete!")
    print(f"Total documents: {len(pdf_files)}")
    print(f"Total chunks: {total_chunks}")
    print(f"Collection: {COLLECTION_NAME}")
    
    # Show collection stats
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"Points in collection: {collection_info.points_count}")

if __name__ == "__main__":
    main()
