# Botboss API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User
```
POST /users/register
Body: {
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "candidate" | "hr" | "admin"
}
```

#### Login
```
POST /users/login?email=user@example.com&password=password123
Response: {
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /users/me
Headers: Authorization: Bearer <token>
```

### Interviews

#### Create Interview
```
POST /interviews/
Body: {
  "candidate_id": 1,
  "role": "developer",
  "scheduled_at": "2024-01-01T10:00:00Z"
}
```

#### Get All Interviews
```
GET /interviews/?skip=0&limit=100
```

#### Get Interview by ID
```
GET /interviews/{interview_id}
```

#### Start Interview
```
POST /interviews/{interview_id}/start
Response: {
  "status": "started",
  "questions": [...]
}
```

#### Submit Response
```
POST /interviews/{interview_id}/responses
Body: {
  "question": "Tell me about yourself",
  "answer": "I am a developer...",
  "question_number": 1
}
```

#### Complete Interview
```
POST /interviews/{interview_id}/complete
Response: {
  "status": "completed",
  "overall_score": 0.85
}
```

### Questions

#### Get Questions
```
GET /questions/?role=developer&category=technical
```

#### Generate AI Questions
```
POST /questions/generate?role=developer&num_questions=5&difficulty=medium
```

### Video

#### Create Video Room
```
POST /video/rooms?room_name=interview_123&max_participants=2
```

#### Generate Access Token
```
POST /video/tokens?room_name=interview_123&identity=user@example.com
Response: {
  "token": "twilio_jwt_token",
  "room_name": "interview_123"
}
```

### Dashboard (HR Only)

#### Get Candidates
```
GET /dashboard/candidates?role=developer&min_score=0.7&status=completed
```

#### Get Statistics
```
GET /dashboard/statistics
Response: {
  "total_interviews": 100,
  "completed_interviews": 85,
  "average_score": 0.82,
  "by_role": [...]
}
```

#### Get Candidate Detail
```
GET /dashboard/candidates/{interview_id}
```

## Response Formats

### Success Response
```json
{
  "id": 1,
  "field": "value"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

