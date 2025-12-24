import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material'
import { Upload as UploadIcon } from '@mui/icons-material'
import { applicationAPI } from '../services/api'

function ApplicationForm() {
  const [formData, setFormData] = useState({
    job_role: '',
    cover_letter: '',
  })
  const [selectedFile, setSelectedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [applicationId, setApplicationId] = useState(null)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                           'text/plain']
      if (!allowedTypes.includes(file.type)) {
        setError('Please upload a PDF, DOC, DOCX, or TXT file')
        return
      }
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('File size must be less than 5MB')
        return
      }
      setSelectedFile(file)
      setError('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      // Create application
      const response = await applicationAPI.create(formData)
      const appId = response.data.id
      setApplicationId(appId)

      // Upload CV if file is selected
      if (selectedFile) {
        await applicationAPI.uploadCV(appId, selectedFile)
        setSuccess('Application submitted and CV uploaded successfully!')
      } else {
        setSuccess('Application submitted successfully!')
      }

      // Redirect after 2 seconds
      setTimeout(() => {
        navigate('/dashboard')
      }, 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit application')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Job Application
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            margin="normal"
            required
            id="job_role"
            name="job_role"
            label="Job Role"
            placeholder="e.g., Developer, Designer, Manager"
            value={formData.job_role}
            onChange={handleChange}
          />

          <TextField
            fullWidth
            margin="normal"
            multiline
            rows={6}
            id="cover_letter"
            name="cover_letter"
            label="Cover Letter (Optional)"
            value={formData.cover_letter}
            onChange={handleChange}
          />

          <Box sx={{ mt: 2, mb: 2 }}>
            <Typography variant="body2" gutterBottom>
              Upload CV/Resume (PDF, DOC, DOCX, or TXT)
            </Typography>
            <Button
              variant="outlined"
              component="label"
              startIcon={<UploadIcon />}
              sx={{ mt: 1 }}
            >
              {selectedFile ? selectedFile.name : 'Choose File'}
              <input
                type="file"
                hidden
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileChange}
              />
            </Button>
            {selectedFile && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                File size: {(selectedFile.size / 1024).toFixed(2)} KB
              </Typography>
            )}
          </Box>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading || !formData.job_role}
          >
            {loading ? <CircularProgress size={24} /> : 'Submit Application'}
          </Button>
        </Box>
      </Paper>
    </Container>
  )
}

export default ApplicationForm

