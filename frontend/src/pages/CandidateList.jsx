import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  TextField,
  MenuItem,
} from '@mui/material'
import { dashboardAPI } from '../services/api'

function CandidateList() {
  const [candidates, setCandidates] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    role: '',
    min_score: '',
    status: '',
  })
  const navigate = useNavigate()

  useEffect(() => {
    fetchCandidates()
  }, [filters])

  const fetchCandidates = async () => {
    try {
      const params = {}
      if (filters.role) params.role = filters.role
      if (filters.min_score) params.min_score = parseFloat(filters.min_score)
      if (filters.status) params.status = filters.status

      const response = await dashboardAPI.getCandidates(params)
      setCandidates(response.data)
    } catch (error) {
      console.error('Error fetching candidates:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      completed: 'success',
      in_progress: 'warning',
      scheduled: 'info',
      cancelled: 'error',
    }
    return colors[status] || 'default'
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Candidates
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} flexWrap="wrap">
          <TextField
            select
            label="Role"
            value={filters.role}
            onChange={(e) => setFilters({ ...filters, role: e.target.value })}
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="developer">Developer</MenuItem>
            <MenuItem value="designer">Designer</MenuItem>
            <MenuItem value="manager">Manager</MenuItem>
          </TextField>
          <TextField
            label="Min Score"
            type="number"
            value={filters.min_score}
            onChange={(e) => setFilters({ ...filters, min_score: e.target.value })}
            sx={{ minWidth: 150 }}
          />
          <TextField
            select
            label="Status"
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="in_progress">In Progress</MenuItem>
            <MenuItem value="scheduled">Scheduled</MenuItem>
          </TextField>
        </Box>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Candidate Name</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Score</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Completed At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {candidates.map((candidate) => (
              <TableRow key={candidate.interview_id} hover>
                <TableCell>{candidate.candidate_name}</TableCell>
                <TableCell>{candidate.role}</TableCell>
                <TableCell>
                  {candidate.overall_score !== null
                    ? `${(candidate.overall_score * 100).toFixed(1)}%`
                    : 'N/A'}
                </TableCell>
                <TableCell>
                  <Chip
                    label={candidate.status}
                    color={getStatusColor(candidate.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {candidate.completed_at
                    ? new Date(candidate.completed_at).toLocaleDateString()
                    : 'N/A'}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => navigate(`/candidates/${candidate.interview_id}`)}
                  >
                    View Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default CandidateList

