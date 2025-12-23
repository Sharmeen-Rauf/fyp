# Botboss Quick Start Guide

## Quick Setup (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"

# Copy environment file
cp env.example .env

# Edit .env and add your OPENAI_API_KEY
# (Minimum required for basic functionality)

# Run the server
python main.py
```

Backend will run on `http://localhost:8000`

### 2. Frontend Setup

```bash
# Open a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 3. First Steps

1. **Register a user**: Go to `http://localhost:3000/register`
   - Create an HR account: role = "hr"
   - Create a candidate account: role = "candidate"

2. **Login**: Use your credentials at `http://localhost:3000/login`

3. **Create an interview** (as HR):
   - Go to Dashboard
   - Create a new interview for a candidate

4. **Take an interview** (as Candidate):
   - Start the interview
   - Answer AI-generated questions
   - View your scores

5. **View results** (as HR):
   - Go to Candidates page
   - View detailed evaluations and scores

## API Testing

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Environment Variables

Minimum required for basic functionality:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional (for full features):
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`: For video interviews
- `DATABASE_URL`: For production database (defaults to SQLite)

## Troubleshooting

**Backend won't start:**
- Check Python version (3.9+)
- Ensure virtual environment is activated
- Verify all dependencies are installed

**Frontend won't start:**
- Check Node.js version (16+)
- Delete `node_modules` and run `npm install` again

**API errors:**
- Verify `.env` file exists in backend directory
- Check that OPENAI_API_KEY is set correctly
- Ensure backend is running on port 8000

**Database errors:**
- SQLite database will be created automatically
- For production, set up PostgreSQL/MySQL and update DATABASE_URL

## Next Steps

1. Read `SETUP.md` for detailed setup instructions
2. Review `PROJECT_STRUCTURE.md` to understand the codebase
3. Check `docs/API.md` for API documentation
4. Customize questions and scoring in `backend/app/services/`

## Support

For issues or questions:
1. Check the documentation files
2. Review error logs in the console
3. Verify all environment variables are set correctly

