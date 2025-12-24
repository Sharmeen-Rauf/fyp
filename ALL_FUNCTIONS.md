# All Functions & Features Overview

## 📍 Current Implementation Status

### ✅ **IMPLEMENTED Functions**

#### 1. **User Management** (`backend/app/api/v1/endpoints/users.py`)
- ✅ `POST /api/v1/users/register` - Register new user
- ✅ `POST /api/v1/users/login` - User login
- ✅ `GET /api/v1/users/me` - Get current user info

#### 2. **Interview Management** (`backend/app/api/v1/endpoints/interviews.py`)
- ✅ `POST /api/v1/interviews/` - Create new interview
- ✅ `GET /api/v1/interviews/` - Get all interviews
- ✅ `GET /api/v1/interviews/{id}` - Get interview by ID
- ✅ `POST /api/v1/interviews/{id}/start` - Start interview (generates AI questions)
- ✅ `POST /api/v1/interviews/{id}/responses` - Submit interview response
- ✅ `POST /api/v1/interviews/{id}/complete` - Complete interview & calculate score

#### 3. **Question Bank** (`backend/app/api/v1/endpoints/questions.py`)
- ✅ `GET /api/v1/questions/` - Get questions from question bank
- ✅ `POST /api/v1/questions/generate` - Generate AI questions dynamically

#### 4. **Video Integration** (`backend/app/api/v1/endpoints/video.py`)
- ✅ `POST /api/v1/video/rooms` - Create video room
- ✅ `POST /api/v1/video/tokens` - Generate video access token
- ✅ `GET /api/v1/video/rooms/{room_sid}` - Get room info

#### 5. **HR Dashboard** (`backend/app/api/v1/endpoints/dashboard.py`)
- ✅ `GET /api/v1/dashboard/candidates` - Get candidates with filters
- ✅ `GET /api/v1/dashboard/statistics` - Get dashboard statistics
- ✅ `GET /api/v1/dashboard/candidates/{id}` - Get candidate details

#### 6. **AI Services** (`backend/app/services/ai/`)
- ✅ `InterviewAgent` - AI agent for question generation & evaluation
- ✅ `SentimentAnalyzer` - Sentiment & behavioral analysis

#### 7. **Scoring System** (`backend/app/services/scoring/`)
- ✅ `ScoringEngine` - Real-time response scoring

#### 8. **Reminder Service** (`backend/app/services/reminder/`)
- ✅ `ReminderService` - Automated reminder system (structure ready)

---

### ✅ **NEWLY ADDED Functions**

#### 1. **CV/Resume Upload** ✅ **NOW IMPLEMENTED**
- ✅ `POST /api/v1/applications/{id}/upload-cv` - Upload CV/resume file
- ✅ Parse CV/resume (extract text from PDF/DOCX/TXT)
- ✅ Store CV/resume in uploads directory
- ✅ View CV/resume via application endpoint
- ✅ CV analysis using AI (OpenAI)

#### 2. **Application Management** ✅ **NOW IMPLEMENTED**
- ✅ `POST /api/v1/applications/` - Create job application
- ✅ `POST /api/v1/applications/{id}/upload-cv` - Submit application with CV
- ✅ `GET /api/v1/applications/` - Get all applications (with filters)
- ✅ `GET /api/v1/applications/{id}` - Get application details
- ✅ `PATCH /api/v1/applications/{id}` - Update application
- ✅ `POST /api/v1/applications/{id}/accept` - Accept application
- ✅ `POST /api/v1/applications/{id}/reject` - Reject application

#### 3. **Additional Features**
- ❌ Email sending (reminder service needs implementation)
- ❌ File storage (for CVs)
- ❌ CV parsing/extraction
- ❌ Job posting management

---

## 📂 **File Locations**

### Backend API Endpoints
```
backend/app/api/v1/endpoints/
├── users.py          → User registration, login
├── interviews.py    → Interview CRUD, responses, scoring
├── questions.py     → Question bank & AI generation
├── video.py         → Video room management
└── dashboard.py     → HR dashboard & analytics
```

### Backend Services
```
backend/app/services/
├── ai/
│   ├── interview_agent.py      → AI question generation & evaluation
│   └── sentiment_analyzer.py   → Sentiment analysis
├── scoring/
│   └── scoring_engine.py       → Response scoring
├── video/
│   └── twilio_service.py       → Video integration
└── reminder/
    └── reminder_service.py    → Reminder system
```

### Frontend Pages
```
frontend/src/pages/
├── Login.jsx           → Login page
├── Register.jsx        → Registration page
├── Dashboard.jsx       → HR dashboard
├── InterviewRoom.jsx   → Interview interface
├── CandidateList.jsx  → Candidate listing
└── CandidateDetail.jsx → Candidate details
```

### Frontend Services
```
frontend/src/services/
└── api.js  → All API calls
```

---

## 🔧 **How to Use Functions**

### 1. **View All API Endpoints**
Visit: `http://localhost:8000/docs` (Swagger UI)

### 2. **Test Functions**
- Use Swagger UI at `/docs`
- Use Postman/Insomnia
- Use frontend pages

### 3. **Check Implementation**
- Backend: `backend/app/api/v1/endpoints/`
- Frontend: `frontend/src/pages/` and `frontend/src/services/api.js`

---

## 🚀 **Next Steps to Add CV/Resume Feature**

I can add:
1. CV upload endpoint
2. CV storage (file system or cloud)
3. CV parsing (extract text from PDF/DOCX)
4. CV analysis using AI
5. Frontend upload component
6. Application management system

Would you like me to implement the CV/resume upload functionality now?

