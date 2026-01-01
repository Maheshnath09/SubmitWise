# ProjectGen - Quick Start Guide

## 🚀 Launch the Application

### Step 1: Start All Services

```bash
cd c:/mysaasapps/Project-Gen-Ai
docker-compose up --build
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (ports 9000, 9001)
- Backend API (port 8000)
- Celery Worker
- Frontend (port 3000)

### Step 2: Wait for Services

Wait approximately 2-3 minutes for all services to initialize. You'll see:
```
✅ Database initialized
✅ Vector store seeded
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

## 🧪 Test the Complete Flow

### 1. Register a New User

1. Go to http://localhost:3000
2. Click "Generate My Project"
3. Click "Sign up"
4. Fill in:
   - Email: test@example.com
   - Password: testpassword123
   - Confirm Password: testpassword123
5. Click "Create Account"

### 2. Complete Onboarding

1. Step 1 - College Information:
   - College Name: Test Engineering College
   - Current Semester: 5
   - Click "Next"

2. Step 2 - Academic Details:
   - Subjects: Computer Networks, DBMS, Web Development
   - Click "Next"

3. Step 3 - Preferences:
   - Language: English
   - Click "Complete Setup"

### 3. Generate a Project

1. Click "Generate New Project" on dashboard
2. Fill in:
   - Subject: Computer Networks
   - Semester: 5
   - Difficulty: Intermediate
   - Additional Requirements: Include network security aspects
3. Click "Generate Project (1 Credit)"

### 4. Monitor Progress

- Status page will auto-refresh every 2 seconds
- Watch progress: pending → processing → completed
- Generation takes approximately 30-60 seconds

### 5. Download Results

1. Click "Preview" to see generated content
2. Click "Download ZIP" to get the bundle
3. Extract ZIP and review:
   - README.md
   - report.docx
   - slides.pptx
   - code/ folder
   - viva_questions.md
   - rubric.md

## 🔧 Run Tests

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

### Frontend Build Test

```bash
cd frontend
npm install
npm run build
```

## 🛠️ Development Mode

### Backend Only

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery Worker

```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

## 📊 Check Service Health

### PostgreSQL
```bash
docker exec -it projectgen-postgres psql -U projectgen -d projectgen -c "\dt"
```

### Redis
```bash
docker exec -it projectgen-redis redis-cli ping
```

### MinIO
Visit http://localhost:9001 and login with minioadmin/minioadmin

### Backend API
Visit http://localhost:8000/health

## 🐛 Troubleshooting

### Services won't start
```bash
docker-compose down -v
docker-compose up --build
```

### Port conflicts
Check if ports 3000, 5432, 6379, 8000, 9000, 9001 are available

### Database issues
```bash
docker-compose down -v  # This will delete all data
docker-compose up --build
```

### Frontend build errors
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

## 📝 Environment Variables

Copy `.env.example` to `.env` and update:
- `JWT_SECRET_KEY` - Change for production
- `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` - For payments
- `STRIPE_SECRET_KEY` - For global payments

## 🎯 What's Working

✅ Complete backend API with Groq integration
✅ RAG pipeline with ChromaDB
✅ DOCX/PPTX/ZIP generation
✅ Authentication & JWT
✅ Celery background tasks
✅ Premium landing page
✅ Full user flow (register → generate → download)
✅ Project status polling
✅ Plagiarism checking

## 🚧 What's Pending

⏳ Admin dashboard UI
⏳ Payment provider integration (structure ready)
⏳ Google OAuth
⏳ Bulk CSV upload
⏳ CI/CD pipeline

## 📞 Need Help?

Check the comprehensive README.md for detailed documentation!
