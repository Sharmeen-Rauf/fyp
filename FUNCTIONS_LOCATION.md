# 📍 All Functions Location Guide

## Complete Function List & Where to Find Them

### 🔐 **Authentication Functions**
**Location:** `backend/app/api/v1/endpoints/users.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `register()` | `/api/v1/users/register` | POST | Register new user |
| `login()` | `/api/v1/users/login` | POST | User login |
| `get_current_user()` | `/api/v1/users/me` | GET | Get current user info |

**Frontend:** `frontend/src/pages/Login.jsx`, `Register.jsx`

---

### 💼 **Interview Functions**
**Location:** `backend/app/api/v1/endpoints/interviews.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `create_interview()` | `/api/v1/interviews/` | POST | Create new interview |
| `get_interviews()` | `/api/v1/interviews/` | GET | Get all interviews |
| `get_interview()` | `/api/v1/interviews/{id}` | GET | Get interview by ID |
| `start_interview()` | `/api/v1/interviews/{id}/start` | POST | Start interview & generate questions |
| `submit_response()` | `/api/v1/interviews/{id}/responses` | POST | Submit answer & get scored |
| `complete_interview()` | `/api/v1/interviews/{id}/complete` | POST | Complete interview & calculate score |

**Frontend:** `frontend/src/pages/InterviewRoom.jsx`

---

### ❓ **Question Functions**
**Location:** `backend/app/api/v1/endpoints/questions.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `get_questions()` | `/api/v1/questions/` | GET | Get questions from bank |
| `generate_questions()` | `/api/v1/questions/generate` | POST | Generate AI questions |

**Service:** `backend/app/services/ai/interview_agent.py` - `InterviewAgent.generate_questions()`

---

### 📹 **Video Functions**
**Location:** `backend/app/api/v1/endpoints/video.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `create_room()` | `/api/v1/video/rooms` | POST | Create video room |
| `generate_token()` | `/api/v1/video/tokens` | POST | Generate access token |
| `get_room()` | `/api/v1/video/rooms/{room_sid}` | GET | Get room info |

**Service:** `backend/app/services/video/twilio_service.py` - `TwilioVideoService`

---

### 📊 **Dashboard Functions (HR Only)**
**Location:** `backend/app/api/v1/endpoints/dashboard.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `get_candidates()` | `/api/v1/dashboard/candidates` | GET | Get candidates with filters |
| `get_statistics()` | `/api/v1/dashboard/statistics` | GET | Get dashboard stats |
| `get_candidate_detail()` | `/api/v1/dashboard/candidates/{id}` | GET | Get candidate details |

**Frontend:** `frontend/src/pages/Dashboard.jsx`, `CandidateList.jsx`, `CandidateDetail.jsx`

---

### 📄 **Application & CV Functions** ✨ **NEW!**
**Location:** `backend/app/api/v1/endpoints/applications.py`

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `create_application()` | `/api/v1/applications/` | POST | Create job application |
| `upload_cv()` | `/api/v1/applications/{id}/upload-cv` | POST | Upload CV/resume file |
| `get_applications()` | `/api/v1/applications/` | GET | Get all applications |
| `get_application()` | `/api/v1/applications/{id}` | GET | Get application details |
| `update_application()` | `/api/v1/applications/{id}` | PATCH | Update application |
| `accept_application()` | `/api/v1/applications/{id}/accept` | POST | Accept application |
| `reject_application()` | `/api/v1/applications/{id}/reject` | POST | Reject application |

**Frontend:** `frontend/src/pages/ApplicationForm.jsx`

**CV Analysis Service:** `backend/app/services/ai/cv_analyzer.py` - `CVAnalyzer`

---

### 🤖 **AI Services**
**Location:** `backend/app/services/ai/`

#### Interview Agent
**File:** `interview_agent.py`
- `generate_questions()` - Generate interview questions
- `evaluate_response()` - Evaluate candidate answers
- `generate_followup_question()` - Generate follow-up questions

#### Sentiment Analyzer
**File:** `sentiment_analyzer.py`
- `analyze()` - Analyze sentiment & behavioral cues
- `_extract_behavioral_cues()` - Extract confidence indicators
- `_calculate_confidence()` - Calculate confidence score
- `_calculate_clarity()` - Calculate clarity score

#### CV Analyzer ✨ **NEW!**
**File:** `cv_analyzer.py`
- `extract_text()` - Extract text from PDF/DOCX/TXT
- `analyze_cv()` - AI analysis of CV content

---

### 📈 **Scoring Functions**
**Location:** `backend/app/services/scoring/scoring_engine.py`

| Function | Description |
|----------|-------------|
| `score_response()` | Score individual response |
| `calculate_interview_score()` | Calculate overall interview score |

---

### 🔔 **Reminder Functions**
**Location:** `backend/app/services/reminder/reminder_service.py`

| Function | Description |
|----------|-------------|
| `create_interview_reminder()` | Create reminder for interview |
| `get_pending_reminders()` | Get pending reminders |
| `send_reminder()` | Send reminder (email/SMS) |
| `process_pending_reminders()` | Process all pending reminders |

---

## 📂 **File Structure Summary**

```
backend/
├── app/
│   ├── api/v1/endpoints/          ← All API endpoints here
│   │   ├── users.py               → Auth functions
│   │   ├── interviews.py          → Interview functions
│   │   ├── questions.py           → Question functions
│   │   ├── video.py               → Video functions
│   │   ├── dashboard.py          → Dashboard functions
│   │   └── applications.py       → Application & CV functions ✨
│   │
│   ├── services/                   ← Business logic here
│   │   ├── ai/
│   │   │   ├── interview_agent.py → AI interview agent
│   │   │   ├── sentiment_analyzer.py → Sentiment analysis
│   │   │   └── cv_analyzer.py     → CV analysis ✨
│   │   ├── scoring/
│   │   │   └── scoring_engine.py  → Scoring logic
│   │   ├── video/
│   │   │   └── twilio_service.py  → Video integration
│   │   └── reminder/
│   │       └── reminder_service.py → Reminder system
│   │
│   └── models/                      ← Database models
│       ├── user.py
│       ├── interview.py
│       ├── question.py
│       ├── reminder.py
│       └── application.py         → Application model ✨

frontend/
├── src/
│   ├── pages/                       ← All pages here
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── InterviewRoom.jsx
│   │   ├── CandidateList.jsx
│   │   ├── CandidateDetail.jsx
│   │   └── ApplicationForm.jsx   → Application form ✨
│   │
│   └── services/
│       └── api.js                  → All API calls
```

---

## 🚀 **How to Use**

### 1. **View All Endpoints**
Visit: `http://localhost:8000/docs` (Swagger UI)

### 2. **Test Functions**
- Use Swagger UI at `/docs`
- Use Postman/Insomnia
- Use frontend pages

### 3. **Add New Functions**
1. Create endpoint in `backend/app/api/v1/endpoints/`
2. Add service logic in `backend/app/services/`
3. Create frontend page in `frontend/src/pages/`
4. Add API call in `frontend/src/services/api.js`

---

## ✅ **Status**

- ✅ **All Core Functions**: Implemented
- ✅ **CV Upload & Analysis**: Implemented ✨
- ✅ **Application Management**: Implemented ✨
- ✅ **Accept/Reject Applications**: Implemented ✨

**Total API Endpoints:** 20+
**Total Frontend Pages:** 7

