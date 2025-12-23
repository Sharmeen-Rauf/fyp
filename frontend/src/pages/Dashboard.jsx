import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material'
import {
  People as PeopleIcon,
  Assignment as AssignmentIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material'
import { dashboardAPI } from '../services/api'
import { useNavigate } from 'react-router-dom'

function Dashboard() {
  const [statistics, setStatistics] = useState(null)
  const [candidates, setCandidates] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [statsRes, candidatesRes] = await Promise.all([
        dashboardAPI.getStatistics(),
        dashboardAPI.getCandidates({ limit: 10 }),
      ])
      setStatistics(statsRes.data)
      setCandidates(candidatesRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
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

  if (loading) {
    return <Typography>Loading...</Typography>
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <PeopleIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Interviews
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.total_interviews || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <AssignmentIcon sx={{ fontSize: 40, color: 'success.main', mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Completed
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.completed_interviews || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <TrendingUpIcon sx={{ fontSize: 40, color: 'warning.main', mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Average Score
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.average_score?.toFixed(2) || '0.00'}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Recent Candidates
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Candidate Name</TableCell>
                <TableCell>Role</TableCell>
                <TableCell>Score</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {candidates.map((candidate) => (
                <TableRow key={candidate.interview_id}>
                  <TableCell>{candidate.candidate_name}</TableCell>
                  <TableCell>{candidate.role}</TableCell>
                  <TableCell>
                    {(candidate.overall_score * 100).toFixed(1)}%
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={candidate.status}
                      color={getStatusColor(candidate.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      size="small"
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
    </Box>
  )
}

export default Dashboard

