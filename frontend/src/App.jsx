import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'

import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import InterviewRoom from './pages/InterviewRoom'
import CandidateList from './pages/CandidateList'
import CandidateDetail from './pages/CandidateDetail'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="interview/:interviewId" element={<InterviewRoom />} />
            <Route path="candidates" element={<CandidateList />} />
            <Route path="candidates/:interviewId" element={<CandidateDetail />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App

