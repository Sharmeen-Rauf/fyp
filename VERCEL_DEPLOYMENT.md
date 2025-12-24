# Vercel Deployment Guide

## Issue Fixed

The 404 error was caused by missing Vercel configuration for Single Page Application (SPA) routing. React Router uses client-side routing, so all routes need to be handled by `index.html`.

## Solution

Two `vercel.json` files have been created:

1. **Root `vercel.json`**: For deploying the entire project
2. **`frontend/vercel.json`**: For deploying only the frontend

## Deployment Options

### Option 1: Deploy Frontend Only (Recommended for now)

If you're deploying just the frontend:

1. In Vercel dashboard, set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

2. The `frontend/vercel.json` will handle routing automatically.

### Option 2: Deploy from Root

If deploying from project root:

1. In Vercel dashboard, set:
   - **Root Directory**: `.` (root)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

2. The root `vercel.json` will handle routing.

## Environment Variables

Add these in Vercel dashboard (Settings → Environment Variables):

```
VITE_API_URL=https://your-backend-url.com/api/v1
```

**Note**: Update this to your actual backend API URL when you deploy the backend.

## Current Configuration

The `vercel.json` files include:
- **Rewrites**: All routes (`/*`) redirect to `/index.html` for SPA routing
- **Headers**: CORS headers for API requests (if needed)

## Testing Locally

To test the build locally:

```bash
cd frontend
npm run build
npm run preview
```

## Next Steps

1. **Redeploy** on Vercel after these changes
2. **Set environment variables** in Vercel dashboard
3. **Update API URL** to point to your deployed backend (when ready)

## Troubleshooting

If you still see 404:
1. Check that `vercel.json` is in the correct location
2. Verify build output directory is `dist`
3. Check Vercel build logs for errors
4. Ensure all routes are working in local preview

