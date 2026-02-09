<div align="center">

# 🎓 SubmitWise

**AI-Powered Semester Project Generator for Indian Engineering & Diploma Students**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://via.placeholder.com/800x400/8B5CF6/FFFFFF?text=ProjectGen+AI+-+Generate+Complete+Projects+in+Minutes" alt="SubmitWise Banner" width="100%">
</p>

[Live Demo](#) • [Documentation](#-api-documentation) • [Quick Start](#-quick-start) • [Architecture](#-system-architecture)

</div>

---

## 🌟 What is SubmitWise?

SubmitWise is a production-ready AI SaaS platform that **generates complete semester project deliverables** for Indian engineering and diploma students. Using **Groq's Llama 3.3 70B** model with RAG (Retrieval-Augmented Generation), it produces professional-grade outputs following **GTU, VTU, AICTE, and Government Polytechnic standards**.

### ✨ What You Get

| Deliverable | Description |
|-------------|-------------|
| 📄 **Project Report (DOCX)** | 8-chapter professional report with IEEE formatting |
| 📊 **Presentation (PPTX)** | 18+ slides covering all aspects |
| 💻 **Source Code** | 5-8 production-ready code files |
| 🎯 **Viva Questions** | 15-20 Q&A with detailed answers |
| 📋 **Test Cases** | Comprehensive testing documentation |
| 📦 **ZIP Bundle** | Everything packaged for submission |

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Frontend (Next.js 14)"
        UI[React Components]
        STORE[Zustand State]
        API_CLIENT[API Client]
    end

    subgraph "Backend (FastAPI)"
        AUTH[Auth API]
        PROJ[Projects API]
        PAY[Payments API]
        ADMIN[Admin API]
    end

    subgraph "AI Engine"
        RAG[RAG Pipeline]
        GROQ[Groq LLM<br/>Llama 3.3 70B]
        EMBED[Embeddings<br/>MiniLM-L6]
        VS[Vector Store<br/>ChromaDB]
    end

    subgraph "Document Generation"
        DOCX[DOCX Generator]
        PPTX[PPTX Generator]
        ZIP[ZIP Bundler]
    end

    subgraph "Infrastructure"
        PG[(PostgreSQL<br/>+ pgvector)]
        REDIS[(Redis)]
        MINIO[(MinIO<br/>S3 Storage)]
        CELERY[Celery Workers]
    end

    UI --> API_CLIENT
    API_CLIENT --> AUTH
    API_CLIENT --> PROJ
    API_CLIENT --> PAY
    
    PROJ --> RAG
    RAG --> EMBED
    RAG --> VS
    RAG --> GROQ
    
    GROQ --> DOCX
    GROQ --> PPTX
    DOCX --> ZIP
    PPTX --> ZIP
    ZIP --> MINIO
    
    AUTH --> PG
    PROJ --> PG
    PROJ --> REDIS
    PROJ --> CELERY
    CELERY --> MINIO

    style GROQ fill:#8B5CF6,color:#fff
    style UI fill:#000,color:#fff
    style PG fill:#336791,color:#fff
    style REDIS fill:#DC382D,color:#fff
    style MINIO fill:#C72C48,color:#fff
```

### 📦 Component Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 14, TypeScript, TailwindCSS | Modern UI with App Router |
| **Backend** | FastAPI, Python 3.11+ | REST API with async support |
| **AI/LLM** | Groq Llama 3.3 70B | Project content generation |
| **RAG** | ChromaDB, Sentence Transformers | Context-aware generation |
| **Database** | PostgreSQL + pgvector | Data persistence + vectors |
| **Queue** | Redis + Celery | Background task processing |
| **Storage** | MinIO (S3-compatible) | File storage with presigned URLs |
| **Payments** | Razorpay, Stripe | Indian & global payments |

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
- **Groq API Key** ([Get free key](https://console.groq.com/))

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/SubmitWise.git
cd SubmitWise

# Copy environment file
cp .env.example .env

# Add your Groq API key in .env
# GROQ_API_KEY=gsk_your_key_here

# Start everything with Docker
docker-compose up -d
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| 🌐 Frontend | http://localhost:3000 | Create account |
| 🔧 API Docs | http://localhost:8000/docs | - |
| 📊 MinIO Console | http://localhost:9001 | minioadmin / minioadmin |

---

## 📂 Project Structure

```
SubmitWise/
├── 📁 backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/                   # REST Endpoints
│   │   │   ├── auth.py           # Authentication routes
│   │   │   ├── projects.py       # Project generation
│   │   │   ├── payments.py       # Payment handling
│   │   │   └── admin.py          # Admin dashboard
│   │   ├── core/                  # Configuration
│   │   │   ├── config.py         # Settings management
│   │   │   ├── database.py       # DB connection
│   │   │   └── security.py       # JWT & hashing
│   │   ├── models/                # SQLAlchemy Models
│   │   │   ├── user.py           # User model
│   │   │   ├── project.py        # Project model
│   │   │   └── payment.py        # Payment model
│   │   ├── services/              # Business Logic
│   │   │   ├── groq_client.py    # 🤖 LLM integration
│   │   │   ├── rag_pipeline.py   # RAG orchestration
│   │   │   ├── vector_store.py   # ChromaDB interface
│   │   │   ├── docx_generator.py # 📄 Report generation
│   │   │   ├── pptx_generator.py # 📊 Slides generation
│   │   │   ├── zip_bundler.py    # 📦 Packaging
│   │   │   └── minio_client.py   # S3 storage
│   │   ├── tasks/                 # Celery Tasks
│   │   │   └── celery_app.py     # Background jobs
│   │   └── main.py               # App entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/                   # Next.js Frontend
│   ├── app/                       # App Router Pages
│   │   ├── (auth)/               # Auth pages
│   │   ├── dashboard/            # User dashboard
│   │   ├── generate/             # Project generation
│   │   ├── projects/             # Project history
│   │   └── pricing/              # Subscription plans
│   ├── components/
│   │   ├── ui/                   # Shadcn components
│   │   └── landing/              # Landing page
│   ├── lib/
│   │   ├── api.ts               # API client
│   │   └── store.ts             # Zustand store
│   └── Dockerfile
│
├── 🐳 docker-compose.yml          # Full stack orchestration
├── 📝 .env.example                # Environment template
└── 📖 README.md                   # This file
```

---

## 🎯 Key Features

### For Students 🎓

- ✅ **2 Free Projects/Month** - No credit card required
- ✅ **Indian Curriculum Focus** - GTU, VTU, AICTE standards
- ✅ **Multiple Difficulty Levels** - Beginner to Advanced
- ✅ **Language Support** - English & Hindi
- ✅ **Complete Code** - 5-8 production-ready files
- ✅ **Viva Preparation** - 15-20 Q&A with answers
- ✅ **Plagiarism Safe** - Unique content generation

### For Colleges 🏫

- ✅ **Bulk Student Onboarding** - CSV upload
- ✅ **Usage Analytics** - Track generation stats
- ✅ **Custom Templates** - Institution-specific formats
- ✅ **Audit Logs** - Complete activity trail

### Technical Features ⚡

- ✅ **RAG-Powered Generation** - Context-aware outputs
- ✅ **Background Processing** - Non-blocking generation
- ✅ **Real-time Status** - Live progress updates
- ✅ **Secure Storage** - Presigned URL downloads
- ✅ **Responsive Design** - Mobile-friendly UI
- ✅ **Dark Mode** - Eye-friendly interface

---

## 🔧 Configuration

### Environment Variables

```env
# Required
GROQ_API_KEY=gsk_your_key_here           # Get from console.groq.com
JWT_SECRET_KEY=your-32-char-secret        # Change in production

# Database (defaults work with Docker)
DATABASE_URL=postgresql://projectgen:projectgen@postgres:5432/projectgen

# Redis
REDIS_URL=redis://redis:6379/0

# MinIO Storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Payments (Optional)
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
STRIPE_SECRET_KEY=your_stripe_key
```

---

## 📚 API Documentation

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Create new account |
| `/api/auth/login` | POST | Login & get tokens |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/me` | GET | Get current user |

### Project Generation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects/generate` | POST | Start project generation |
| `/api/projects/{id}/status` | GET | Check generation progress |
| `/api/projects/{id}/preview` | GET | Get JSON preview |
| `/api/projects/{id}/download` | GET | Download ZIP bundle |
| `/api/projects/history` | GET | List user's projects |

### Interactive Docs

Visit **http://localhost:8000/docs** for Swagger UI with try-it-out functionality.

---

## 🛠️ Development Setup

### Backend (Python)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Node.js)

```bash
cd frontend
npm install
npm run dev
```

### Run Services (Docker)

```bash
# Start only database services
docker-compose up postgres redis minio -d
```

---

## 🚢 Production Deployment

### Docker Compose

```bash
# Build and run all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Environment Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random string
- [ ] Set up production PostgreSQL
- [ ] Configure Redis cluster
- [ ] Set up MinIO with proper credentials
- [ ] Add payment provider keys
- [ ] Set `DEBUG=false`

---

## 📊 Tech Stack Summary

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Frontend** | Next.js 14, TypeScript, TailwindCSS, Zustand, Framer Motion |
| **Backend** | FastAPI, Python 3.11, Pydantic, SQLAlchemy |
| **AI/ML** | Groq Llama 3.3 70B, Sentence Transformers, ChromaDB |
| **Database** | PostgreSQL 15, pgvector, Redis 7 |
| **DevOps** | Docker, Docker Compose, Celery |
| **Storage** | MinIO (S3-compatible) |
| **Payments** | Razorpay, Stripe |

</div>

---

## 🗺️ Roadmap

- [ ] 🔐 Google OAuth / SSO
- [ ] 📱 Mobile Application
- [ ] 🌍 More Languages (Tamil, Telugu, Marathi)
- [ ] 🔌 API Access for Enterprises
- [ ] 📈 Advanced Analytics Dashboard
- [ ] 🤝 Collaborative Editing

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

```bash
# Fork the repo
# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

- 📧 **Email**: [support@SubmitWise](mailto:support@SubmitWise)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/projectgen-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/projectgen-ai/discussions)

---

<div align="center">

**Made with ❤️ for Indian Engineering Students**

⭐ Star this repo if you find it helpful!

</div>
