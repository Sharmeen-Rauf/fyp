# Botboss Project Structure

## Overview

Botboss is an AI-driven virtual interview system with a clear separation between frontend and backend.

## Directory Structure

```
botboss/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── v1/
│   │   │       ├── endpoints/ # API endpoint handlers
│   │   │       │   ├── users.py
│   │   │       │   ├── interviews.py
│   │   │       │   ├── questions.py
│   │   │       │   ├── video.py
│   │   │       │   └── dashboard.py
│   │   │       └── api.py     # API router
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Settings and environment variables
│   │   │   ├── database.py     # Database connection
│   │   │   └── security.py    # Authentication and security
│   │   ├── models/            # SQLAlchemy database models
│   │   │   ├── user.py
│   │   │   ├── interview.py
│   │   │   ├── question.py
│   │   │   └── reminder.py
│   │   ├── schemas/           # Pydantic schemas for validation
│   │   │   ├── user.py
│   │   │   └── interview.py
│   │   └── services/          # Business logic services
│   │       ├── ai/            # AI services
│   │       │   ├── interview_agent.py    # AI interview agent
│   │       │   └── sentiment_analyzer.py  # Sentiment analysis
│   │       ├── scoring/       # Scoring services
│   │       │   └── scoring_engine.py
│   │       ├── video/         # Video integration
│   │       │   └── twilio_service.py
│   │       └── reminder/      # Reminder service
│   │           └── reminder_service.py
│   ├── tests/                 # Backend tests
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt       # Python dependencies
│   └── env.example          # Environment variables template
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   │   └── Layout.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── InterviewRoom.jsx
│   │   │   ├── CandidateList.jsx
│   │   │   └── CandidateDetail.jsx
│   │   ├── services/        # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
│
├── docs/                     # Documentation
│   └── API.md               # API documentation
│
├── README.md                # Project overview
├── SETUP.md                 # Setup instructions
├── PROJECT_STRUCTURE.md     # This file
└── .gitignore              # Git ignore rules
```

## Key Components

### Backend

#### API Layer (`app/api/v1/endpoints/`)
- **users.py**: User registration, login, authentication
- **interviews.py**: Interview creation, management, response submission
- **questions.py**: Question bank and AI question generation
- **video.py**: Video room creation and token generation
- **dashboard.py**: HR dashboard endpoints (candidates, statistics)

#### Core (`app/core/`)
- **config.py**: Application settings from environment variables
- **database.py**: SQLAlchemy database session management
- **security.py**: JWT authentication, password hashing

#### Models (`app/models/`)
- **user.py**: User model with roles (admin, hr, candidate)
- **interview.py**: Interview and InterviewResponse models
- **question.py**: Question bank model
- **reminder.py**: Reminder model for automated notifications

#### Services (`app/services/`)
- **ai/interview_agent.py**: Agentic AI for interview management and question generation
- **ai/sentiment_analyzer.py**: NLP-based sentiment and behavioral analysis
- **scoring/scoring_engine.py**: Response scoring algorithm
- **video/twilio_service.py**: Twilio video integration
- **reminder/reminder_service.py**: Automated reminder system

### Frontend

#### Pages (`src/pages/`)
- **Login.jsx**: User authentication
- **Register.jsx**: User registration
- **Dashboard.jsx**: HR dashboard with statistics
- **InterviewRoom.jsx**: Interview interface for candidates
- **CandidateList.jsx**: List of candidates with filtering
- **CandidateDetail.jsx**: Detailed candidate evaluation

#### Services (`src/services/`)
- **api.js**: Centralized API client with authentication

## Data Flow

1. **User Registration/Login**: Frontend → API → Database → JWT Token
2. **Interview Creation**: HR → API → Database → Interview Record
3. **Interview Process**: 
   - Candidate starts interview → AI generates questions
   - Candidate submits answers → Sentiment analysis → Scoring → Database
4. **Dashboard**: HR → API → Database → Aggregated statistics and candidate list

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **OpenAI API**: GPT-4 for question generation and evaluation
- **spaCy/NLTK**: NLP and sentiment analysis
- **Twilio**: Video conferencing
- **JWT**: Authentication

### Frontend
- **React**: UI library
- **Material-UI**: Component library
- **Vite**: Build tool
- **Axios**: HTTP client
- **React Router**: Routing

## Database Schema

### Users
- id, email, hashed_password, full_name, role, is_active, timestamps

### Interviews
- id, candidate_id, hr_id, role, status, scores, timestamps

### Interview Responses
- id, interview_id, question, answer, scores (sentiment, confidence, clarity, relevance), analysis data

### Question Bank
- id, role, category, question, expected_keywords, difficulty

### Reminders
- id, interview_id, candidate_id, reminder_type, scheduled_time, status

