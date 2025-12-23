# Botboss - AI-Driven Virtual Interview System

## Project Overview

Botboss is an intelligent candidate shortlisting system that automates the interview process using AI. The system conducts virtual interviews, evaluates candidate responses using NLP and sentiment analysis, and provides data-driven insights to HR departments.

## Features

1. **Automated Interviewing**: AI bot conducts interviews with pre-set or dynamically generated questions
2. **Behavioral and Sentiment Analysis**: Evaluates tone, confidence, and clarity
3. **Real-time Scoring System**: Scores responses instantly using NLP
4. **Agentic AI Implementation**: Advanced AI agent for interview management
5. **Role-Based Question Bank**: Custom interview flows for different roles
6. **HR Dashboard**: Centralized dashboard for viewing candidate scores and reports
7. **Data Privacy & Secure Storage**: Encrypted cloud storage for all data
8. **Reminder System**: Automated reminders for candidates
9. **AI-Driven Scoring**: Objective candidate evaluation using AI metrics

## Technology Stack

### Frontend
- React.js / React Native
- Material-UI / Ant Design
- Axios for API calls

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy ORM

### AI/NLP
- OpenAI API (GPT-4)
- spaCy
- NLTK
- Sentiment Analysis libraries

### Database
- SQLite (Development)
- PostgreSQL / MySQL (Production)
- MongoDB (Optional for document storage)

### Video API
- Twilio Video API
- WebRTC

### Hosting
- AWS / Vercel / Firebase

## Project Structure

```
botboss/
├── backend/                 # Python backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   │   ├── ai/         # AI/NLP services
│   │   │   ├── video/      # Video integration
│   │   │   └── scoring/    # Scoring algorithms
│   │   ├── schemas/        # Pydantic schemas
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom hooks
│   │   ├── utils/          # Utility functions
│   │   └── App.js          # Main app component
│   ├── public/             # Static files
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
└── .env.example           # Environment variables template
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Environment Variables

Create a `.env` file in the backend directory with:

```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./botboss.db
SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
FRONTEND_URL=http://localhost:3000
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Phases

- **Phase 1 (Aug - Sept)**: Research, Dataset collection, Model integration
- **Phase 2 (Oct - Nov)**: Frontend + Backend Development, Video Module
- **Phase 3 (Dec)**: Testing, Optimization, Final Deployment

## License

This project is part of a Final Year Project (FYP).

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Twilio Video API](https://www.twilio.com/docs/video)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

