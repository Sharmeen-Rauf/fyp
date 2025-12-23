# Botboss Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn
- PostgreSQL/MySQL (optional, SQLite used by default)
- OpenAI API key
- Twilio account (for video features)

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install spaCy language model
```bash
python -m spacy download en_core_web_sm
```

### 5. Download NLTK data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

### 6. Configure environment variables
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional: TWILIO credentials for video features
```

### 7. Initialize database
The database will be created automatically on first run. For production, use PostgreSQL or MySQL:

```python
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/botboss
```

### 8. Run the server
```bash
python main.py
# Or
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
# Or
yarn install
```

### 3. Configure environment (optional)
Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 4. Start development server
```bash
npm run dev
# Or
yarn dev
```

The frontend will be available at `http://localhost:3000`

## Database Migrations (Optional)

If you want to use Alembic for database migrations:

```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Production Deployment

### Backend
1. Set `ENVIRONMENT=production` in `.env`
2. Use a production WSGI server:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `dist` folder using a web server (nginx, Apache, etc.)

## Troubleshooting

### Common Issues

1. **OpenAI API Error**: Make sure your API key is set correctly in `.env`
2. **Database Error**: Ensure the database URL is correct and the database exists
3. **Import Errors**: Make sure all dependencies are installed and virtual environment is activated
4. **CORS Error**: Check that `FRONTEND_URL` in backend `.env` matches your frontend URL

### Getting Help

- Check the API documentation at `/docs` endpoint
- Review error logs in the console
- Ensure all environment variables are set correctly

