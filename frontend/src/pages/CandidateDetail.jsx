import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Grid,
  Chip,
  CircularProgress,
} from '@mui/material'
import { dashboardAPI } from '../services/api'

function CandidateDetail() {
  const { interviewId } = useParams()
  const [interview, setInterview] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCandidateDetail()
  }, [interviewId])

  const fetchCandidateDetail = async () => {
    try {
      const response = await dashboardAPI.getCandidateDetail(interviewId)
      setInterview(response.data)
    } catch (error) {
      console.error('Error fetching candidate detail:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  if (!interview) {
    return <Typography>Candidate not found</Typography>
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Candidate Details
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Overview
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Candidate: {interview.candidate?.full_name || 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Role: {interview.role}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Status: <Chip label={interview.status} size="small" />
              </Typography>
              <Typography variant="h5" sx={{ mt: 2 }}>
                Overall Score: {(interview.overall_score * 100).toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Interview Responses
            </Typography>
            {interview.responses && interview.responses.length > 0 ? (
              interview.responses.map((response, index) => (
                <Card key={response.id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Question {response.question_number}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {response.question}
                    </Typography>
                    <Typography variant="body1" paragraph>
                      <strong>Answer:</strong> {response.answer}
                    </Typography>
                    <Box display="flex" gap={2} flexWrap="wrap" sx={{ mt: 2 }}>
                      <Chip
                        label={`Sentiment: ${(response.sentiment_score * 100).toFixed(1)}%`}
                        size="small"
                      />
                      <Chip
                        label={`Confidence: ${(response.confidence_score * 100).toFixed(1)}%`}
                        size="small"
                      />
                      <Chip
                        label={`Clarity: ${(response.clarity_score * 100).toFixed(1)}%`}
                        size="small"
                      />
                      <Chip
                        label={`Score: ${(response.overall_score * 100).toFixed(1)}%`}
                        size="small"
                        color="primary"
                      />
                    </Box>
                    {response.ai_feedback && (
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                        <strong>AI Feedback:</strong> {response.ai_feedback}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              ))
            ) : (
              <Typography>No responses available</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default CandidateDetail

