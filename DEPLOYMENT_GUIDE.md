# 🚀 Pokemon Search & Sim - Deployment Guide

## 📋 Overview
This guide will help you deploy your Pokemon Search & Sim app for **FREE** using:
- **Frontend**: Vercel (Free)
- **Backend**: Render (Free tier)
- **Database**: Qdrant Cloud (Already set up)

**Total Cost: $0/month** 🎉

## 🔧 Prerequisites
- GitHub account
- Your domain name
- Qdrant Cloud credentials (already have)

## 📦 Step 1: Prepare Your Code

### 1.1 Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Ready for deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/pokemon-search-and-sim.git
git branch -M main
git push -u origin main
```

## 🎯 Step 2: Deploy Backend (Render)

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your GitHub account

### 2.2 Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `pokemon-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn api:app --host 0.0.0.0 --port $PORT`

### 2.3 Set Environment Variables
In Render dashboard, add:
```
QDRANT_API_KEY = your_actual_qdrant_api_key
QDRANT_URL = your_actual_qdrant_url
```

### 2.4 Deploy
- Click **"Create Web Service"**
- Wait for deployment (5-10 minutes)
- Note your backend URL: `https://pokemon-api-xxxx.onrender.com`

## 🌐 Step 3: Deploy Frontend (Vercel)

### 3.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### 3.2 Deploy Frontend
1. Click **"New Project"**
2. Import your GitHub repo
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3.3 Set Environment Variables
In Vercel dashboard → Settings → Environment Variables:
```
VITE_API_BASE_URL = https://pokemon-api-xxxx.onrender.com
```
(Use your actual Render backend URL)

### 3.4 Deploy
- Click **"Deploy"**
- Wait for deployment (2-3 minutes)
- Your app is live at: `https://your-app-xxxx.vercel.app`

## 🌍 Step 4: Add Your Custom Domain

### 4.1 In Vercel Dashboard
1. Go to your project → Settings → Domains
2. Add your domain: `yourdomain.com`
3. Follow DNS instructions

### 4.2 DNS Configuration
Add these records to your domain:
```
Type: A
Name: @
Value: 76.76.19.61

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

## ✅ Step 5: Test Your Deployment

### 5.1 Test Backend
```bash
curl https://pokemon-api-xxxx.onrender.com/health
# Should return: {"status":"healthy"}
```

### 5.2 Test Frontend
Visit your domain and test:
- Pokemon search
- Battle simulation
- Rankings

## 🔧 Troubleshooting

### Backend Issues
- **503 Error**: Render free tier sleeps after 15min inactivity
- **Environment Variables**: Double-check Qdrant credentials
- **Logs**: Check Render dashboard → Logs

### Frontend Issues
- **API Errors**: Verify `VITE_API_BASE_URL` is correct
- **CORS Issues**: Backend should allow your domain
- **Build Errors**: Check Vercel build logs

## 🚀 Going Live Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel  
- [ ] Environment variables set correctly
- [ ] Custom domain configured
- [ ] SSL certificate active (automatic)
- [ ] All features tested on production

## 💡 Pro Tips

### Performance
- Render free tier sleeps after 15min → First request may be slow
- Consider upgrading to Render paid plan ($7/month) for no sleep

### Monitoring
- Set up Render health checks
- Monitor Vercel analytics
- Check Qdrant usage in their dashboard

### Updates
- Push to GitHub → Auto-deploys to both platforms
- Use Vercel preview deployments for testing

## 🎉 You're Live!

Your Pokemon Search & Sim app is now live at your custom domain with:
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ SSL certificates
- ✅ Global CDN (Vercel)
- ✅ Professional setup

**Estimated setup time: 30-45 minutes**
