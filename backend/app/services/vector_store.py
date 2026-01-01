import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.embeddings import embedding_service
import uuid


class VectorStore:
    """Vector store using ChromaDB for RAG"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.collection_name = "project_templates"
    
    def initialize(self):
        """Initialize ChromaDB client and collection"""
        if self.client is None:
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Project templates and examples for RAG"}
            )
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ):
        """Add documents to vector store"""
        self.initialize()
        
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Generate embeddings
        embeddings = embedding_service.embed_batch(texts)
        
        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        self.initialize()
        
        if top_k is None:
            top_k = settings.RAG_TOP_K
        
        # Generate query embedding
        query_embedding = embedding_service.embed_text(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'score': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                })
        
        return formatted_results
    
    def seed_templates(self):
        """Seed initial project templates for RAG"""
        self.initialize()
        
        # Check if already seeded
        if self.collection.count() > 0:
            return
        
        # Sample templates for Indian college projects
        templates = [
            {
                "text": """Computer Networks Project: Network Traffic Analyzer
                Abstract: A network packet analyzer tool that captures and analyzes network traffic in real-time. 
                Modules: Packet Capture (2 weeks), Protocol Analysis (3 weeks), Visualization Dashboard (2 weeks)
                Tech Stack: Python, Scapy, Wireshark, Flask, Chart.js
                Difficulty: Intermediate""",
                "metadata": {"subject": "Computer Networks", "difficulty": "Intermediate"}
            },
            {
                "text": """Web Development Project: E-Commerce Platform
                Abstract: A full-stack e-commerce website with product catalog, shopping cart, and payment integration.
                Modules: User Authentication (2 weeks), Product Management (3 weeks), Cart & Checkout (2 weeks), Payment Gateway (1 week)
                Tech Stack: React, Node.js, Express, MongoDB, Razorpay
                Difficulty: Advanced""",
                "metadata": {"subject": "Web Development", "difficulty": "Advanced"}
            },
            {
                "text": """Database Management Project: Library Management System
                Abstract: A database-driven application for managing library operations including book inventory and member records.
                Modules: Database Design (2 weeks), CRUD Operations (2 weeks), Search & Reports (2 weeks)
                Tech Stack: MySQL, PHP, HTML/CSS, Bootstrap
                Difficulty: Beginner""",
                "metadata": {"subject": "DBMS", "difficulty": "Beginner"}
            },
            {
                "text": """Machine Learning Project: Student Performance Predictor
                Abstract: ML model to predict student academic performance based on various factors.
                Modules: Data Collection (1 week), Data Preprocessing (2 weeks), Model Training (2 weeks), Web Interface (2 weeks)
                Tech Stack: Python, Scikit-learn, Pandas, Flask, Matplotlib
                Difficulty: Intermediate""",
                "metadata": {"subject": "Machine Learning", "difficulty": "Intermediate"}
            },
            {
                "text": """Operating Systems Project: Process Scheduler Simulator
                Abstract: Simulation of various CPU scheduling algorithms with performance comparison.
                Modules: Algorithm Implementation (3 weeks), Simulation Engine (2 weeks), Visualization (2 weeks)
                Tech Stack: C++, Qt, Matplotlib
                Difficulty: Intermediate""",
                "metadata": {"subject": "Operating Systems", "difficulty": "Intermediate"}
            },
            {
                "text": """IoT Project: Smart Home Automation
                Abstract: IoT-based home automation system with sensor integration and mobile control.
                Modules: Sensor Integration (2 weeks), Microcontroller Programming (3 weeks), Mobile App (2 weeks), Cloud Integration (1 week)
                Tech Stack: Arduino, ESP8266, MQTT, React Native, Firebase
                Difficulty: Advanced""",
                "metadata": {"subject": "IoT", "difficulty": "Advanced"}
            }
        ]
        
        texts = [t["text"] for t in templates]
        metadatas = [t["metadata"] for t in templates]
        
        self.add_documents(texts, metadatas)


# Singleton instance
vector_store = VectorStore()
