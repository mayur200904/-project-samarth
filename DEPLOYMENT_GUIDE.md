# 🚀 Project Samarth - Deployment Guide

## Quick Deploy Options

You have several options to deploy your working Q&A system:

---

## Option 1: Vercel (Recommended - Easiest & Free) ⭐

### Why Vercel?
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy setup (5 minutes)
- ✅ Great for React/Vite apps
- ✅ GitHub integration

### Steps:

#### A. Prepare Frontend for Production

1. **Update API URL for production:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
```

Create `.env.production`:
```bash
cat > .env.production << 'EOF'
VITE_API_URL=https://your-backend-url.com/api/v1
EOF
```

2. **Test production build:**
```bash
npm run build
npm run preview
```

#### B. Deploy to Vercel

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Deploy:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
vercel
```

Follow prompts:
- Project name: `project-samarth`
- Framework: `Vite`
- Build command: `npm run build`
- Output directory: `dist`

4. **Get your URL:**
After deployment, you'll get a URL like: `https://project-samarth.vercel.app`

---

## Option 2: Railway (Backend + Frontend Together) 🚂

### Why Railway?
- ✅ Free tier: 500 hours/month
- ✅ Deploy both frontend and backend
- ✅ PostgreSQL support if needed
- ✅ Environment variables management

### Steps:

1. **Sign up:** https://railway.app
2. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

3. **Login:**
```bash
railway login
```

4. **Deploy Backend:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/backend
railway init
railway up
```

5. **Deploy Frontend:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
railway init
railway up
```

---

## Option 3: Render (All-in-One) 🎨

### Why Render?
- ✅ Free tier for web services
- ✅ Good for Python + Node.js
- ✅ Auto-deploy from GitHub
- ✅ Built-in PostgreSQL

### Steps:

1. **Push to GitHub:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice
git init
git add .
git commit -m "Initial commit"
gh repo create project-samarth --public --source=. --push
```

2. **Go to:** https://render.com
3. **Create New Web Service** (for backend)
   - Connect GitHub repo
   - Build command: `cd backend && pip install -r requirements.txt`
   - Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Create Static Site** (for frontend)
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

---

## Option 4: Simple VM/VPS (DigitalOcean, AWS, etc.) 💻

### For Full Control

1. **Get a server** (DigitalOcean Droplet, AWS EC2, etc.)

2. **Install dependencies:**
```bash
# Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs
```

3. **Clone your code:**
```bash
git clone your-repo
cd project-samarth
```

4. **Setup backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Setup frontend:**
```bash
cd ../frontend
npm install
npm run build
```

6. **Run with PM2:**
```bash
npm install -g pm2

# Backend
pm2 start "cd ~/project-samarth/backend && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000" --name backend

# Frontend (serve static files)
pm2 serve ~/project-samarth/frontend/dist 5173 --name frontend
```

7. **Setup Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

---

## Fastest Option: Just Deploy Frontend (Use Local Backend) ⚡

If you just want to deploy the UI quickly for demo purposes:

### Steps:

1. **Make simple.html standalone:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
```

2. **Create production build:**
```bash
npm run build
```

3. **Deploy to Netlify (Drag & Drop):**
   - Go to: https://app.netlify.com/drop
   - Drag the `dist` folder
   - Done! Get instant URL

4. **Update API URL:**
   - You'll need to expose your local backend using ngrok
   - Or deploy backend separately

---

## RECOMMENDED APPROACH FOR QUICK DEMO 🎯

### Use Ngrok to Expose Local Backend + Deploy Frontend

1. **Install ngrok:**
```bash
brew install ngrok
```

2. **Expose backend:**
```bash
ngrok http 8000
```
You'll get URL like: `https://abc123.ngrok.io`

3. **Update frontend API URL:**
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
echo "VITE_API_URL=https://abc123.ngrok.io/api/v1" > .env.production
```

4. **Build frontend:**
```bash
npm run build
```

5. **Deploy to Netlify:**
   - Go to https://app.netlify.com/drop
   - Drag `dist` folder
   - Get shareable URL!

**Now you can access your Q&A system from anywhere!**

---

## Environment Variables Needed

### Backend (.env)
```env
OPENAI_API_KEY=your_key_here
DATA_GOV_API_KEY=your_key_here
ENVIRONMENT=production
```

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend-url.com/api/v1
```

---

## Cost Comparison

| Platform | Backend | Frontend | Total/Month |
|----------|---------|----------|-------------|
| **Vercel + Railway** | $0 (500h) | $0 | **$0** |
| **Render** | $0 (750h) | $0 | **$0** |
| **Netlify + Ngrok** | Local | $0 | **$0** |
| **DigitalOcean** | $6 | Included | **$6** |
| **AWS** | ~$5-10 | ~$1 | **$6-11** |

---

## What I Recommend For You 🎯

**For Quick Demo (Next 1 Hour):**
1. Use **Ngrok** for backend (keeps it local, instant setup)
2. Deploy frontend to **Netlify Drop** (literally drag & drop)
3. Share the Netlify URL with anyone

**For Competition Submission (Production):**
1. Deploy backend to **Railway** (free, easy)
2. Deploy frontend to **Vercel** (free, professional)
3. Use your own domain (optional)

---

## Ready to Deploy?

Let me know which option you prefer, and I'll create the exact commands and scripts you need!

Quick recommendation: **Ngrok + Netlify** is the fastest (5 minutes total)!
