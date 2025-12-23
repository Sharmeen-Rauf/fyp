import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Grid,
} from '@mui/material'
import { interviewAPI, videoAPI } from '../services/api'

function InterviewRoom() {
  const { interviewId } = useParams()
  const navigate = useNavigate()
  const [interview, setInterview] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [questionNumber, setQuestionNumber] = useState(0)
  const [answer, setAnswer] = useState('')
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const videoRef = useRef(null)

  useEffect(() => {
    loadInterview()
  }, [interviewId])

  const loadInterview = async () => {
    try {
      const response = await interviewAPI.getById(interviewId)
      setInterview(response.data)
      
      // Start interview if not started
      if (response.data.status === 'scheduled') {
        await startInterview()
      } else {
        setLoading(false)
      }
    } catch (err) {
      setError('Failed to load interview')
      setLoading(false)
    }
  }

  const startInterview = async () => {
    try {
      const response = await interviewAPI.start(interviewId)
      setQuestions(response.data.questions || [])
      if (response.data.questions && response.data.questions.length > 0) {
        setCurrentQuestion(response.data.questions[0])
        setQuestionNumber(1)
      }
      setLoading(false)
    } catch (err) {
      setError('Failed to start interview')
      setLoading(false)
    }
  }

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer')
      return
    }

    setSubmitting(true)
    setError('')

    try {
      await interviewAPI.submitResponse(interviewId, {
        question: currentQuestion.question || currentQuestion,
        answer: answer,
        question_number: questionNumber,
      })

      // Move to next question
      if (questionNumber < questions.length) {
        setCurrentQuestion(questions[questionNumber])
        setQuestionNumber(questionNumber + 1)
        setAnswer('')
      } else {
        // Complete interview
        await completeInterview()
      }
    } catch (err) {
      setError('Failed to submit answer')
    } finally {
      setSubmitting(false)
    }
  }

  const completeInterview = async () => {
    try {
      await interviewAPI.complete(interviewId)
      navigate('/dashboard')
    } catch (err) {
      setError('Failed to complete interview')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Interview Room
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Question {questionNumber} of {questions.length}
              </Typography>
              <Typography variant="body1" paragraph>
                {typeof currentQuestion === 'string' 
                  ? currentQuestion 
                  : currentQuestion?.question || 'No question available'}
              </Typography>

              <TextField
                fullWidth
                multiline
                rows={6}
                label="Your Answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                sx={{ mt: 2 }}
              />

              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleSubmitAnswer}
                  disabled={submitting || !answer.trim()}
                >
                  {submitting ? 'Submitting...' : questionNumber < questions.length ? 'Next Question' : 'Complete Interview'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Interview Info
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Role: {interview?.role}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Status: {interview?.status}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default InterviewRoom

