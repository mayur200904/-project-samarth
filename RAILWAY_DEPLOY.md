# 🚀 RAILWAY DEPLOYMENT GUIDE
## Easiest Way to Deploy with GitHub Student Developer Pack!

---

## 🎁 What You Get with Railway + Student Pack:
- ✅ **$5/month credit** (FREE!)
- ✅ **Backend deployed** (FastAPI + Python)
- ✅ **Automatic HTTPS**
- ✅ **Environment variables** management
- ✅ **Auto-deploy** from Git
- ✅ **Custom domain** support

---

## 📋 Prerequisites Checklist:
- [x] Backend working locally ✅
- [x] Simple UI working ✅
- [x] GitHub Student Developer Pack activated
- [ ] Railway account (we'll create this)

---

## 🚀 DEPLOYMENT STEPS (15 Minutes Total!)

### Step 1: Prepare Files (2 minutes)

Run this script to create all necessary files:

```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice
chmod +x prepare-railway.sh
./prepare-railway.sh
```

This creates:
- ✅ `frontend/standalone-simple.html` - Your simple UI
- ✅ Backend Railway configuration files
- ✅ Git repository (if not exists)

---

### Step 2: Sign Up for Railway (3 minutes)

1. **Go to:** https://railway.app

2. **Click "Login with GitHub"**

3. **Connect your GitHub Student Pack:**
   - Go to: https://railway.app/account
   - Verify student email
   - Get $5/month credit!

---

### Step 3: Deploy Backend to Railway (5 minutes)

#### Option A: Using Railway Website (Easier)

1. **Go to:** https://railway.app/new

2. **Click "Deploy from GitHub repo"**

3. **Authorize Railway** to access your GitHub

4. **Select your repository** (or create new one first - see Step 3B)

5. **Railway will detect Python automatically!**

6. **Add Environment Variables:**
   - Click "Variables"
   - Add these:
     ```
     OPENAI_API_KEY=your_openai_key_here
     DATA_GOV_API_KEY=your_data_gov_key_here
     ENVIRONMENT=production
     PORT=8000
     ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** for deployment

9. **Get your URL:** 
   - Click "Settings" → "Generate Domain"
   - You'll get something like: `https://your-app.up.railway.app`

#### Option B: Using Railway CLI (For Advanced Users)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend
cd /Users/mayursantoshtarate/Desktop/Apperentice/backend

# Initialize Railway project
railway init

# Add environment variables
railway variables set OPENAI_API_KEY="your_key_here"
railway variables set DATA_GOV_API_KEY="your_key_here"
railway variables set ENVIRONMENT="production"

# Deploy!
railway up

# Get your URL
railway open
```

---

### Step 4: Update Frontend with Backend URL (2 minutes)

1. **Copy your Railway backend URL**
   Example: `https://project-samarth-production.up.railway.app`

2. **Update standalone-simple.html:**

   Open: `/Users/mayursantoshtarate/Desktop/Apperentice/frontend/standalone-simple.html`

   Find this line (around line 101):
   ```javascript
   const API_URL = 'REPLACE_WITH_YOUR_RAILWAY_BACKEND_URL/api/v1';
   ```

   Replace with your actual URL:
   ```javascript
   const API_URL = 'https://your-app.up.railway.app/api/v1';
   ```

3. **Save the file!**

---

### Step 5: Deploy Frontend to Netlify (3 minutes)

#### Option A: Netlify Drop (Easiest!)

1. **Go to:** https://app.netlify.com/drop

2. **Drag `standalone-simple.html`** onto the page
   - Location: `/Users/mayursantoshtarate/Desktop/Apperentice/frontend/standalone-simple.html`

3. **Rename it:** Click the three dots → Site settings → Change site name

4. **Done!** You get a URL like: `https://project-samarth.netlify.app`

#### Option B: Netlify as index.html

```bash
# Create a deploy folder
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
mkdir -p deploy
cp standalone-simple.html deploy/index.html

# Drag the 'deploy' folder to https://app.netlify.com/drop
```

---

## ✅ VERIFICATION STEPS

### Test Your Backend:
```bash
curl https://your-app.up.railway.app/api/v1/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0",...}
```

### Test Your Frontend:
1. Open your Netlify URL
2. Type: "Compare rice production in Punjab and West Bengal"
3. Click "Ask"
4. Wait ~25 seconds
5. See answer with citations! 🎉

---

## 🎯 FINAL URLS

After deployment, you'll have:

**Backend (Railway):**
```
https://your-app.up.railway.app/api/v1
```

**Frontend (Netlify):**
```
https://project-samarth.netlify.app
```

**Both accessible from ANY device, ANYWHERE in the world! 🌍**

---

## 🐛 TROUBLESHOOTING

### Backend Issues:

**"Application failed to start"**
- Check Railway logs: Dashboard → Deployments → View logs
- Verify environment variables are set
- Check `requirements.txt` is correct

**"Module not found"**
- Make sure `requirements.txt` includes all dependencies
- Redeploy from Railway dashboard

### Frontend Issues:

**"Failed to get response from backend"**
- Check API_URL in `standalone-simple.html` is correct
- Verify backend is running (check Railway dashboard)
- Check browser console for CORS errors

**CORS Errors:**
Add this to `backend/app/main.py` (after imports):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy backend after adding this.

---

## 💰 COST

**Total Monthly Cost:**
- Railway Backend: **$0** (covered by $5 student credit)
- Netlify Frontend: **$0** (free tier)
- **Total: $0/month** 🎉

---

## 🚀 QUICK COMMANDS REFERENCE

### Prepare deployment:
```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice
./prepare-railway.sh
```

### Check backend locally:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
curl http://localhost:8000/api/v1/health
```

### Deploy backend (CLI method):
```bash
cd backend
railway login
railway init
railway up
```

### Get Railway backend URL:
```bash
railway open
```

---

## 📝 POST-DEPLOYMENT CHECKLIST

- [ ] Backend deployed to Railway ✓
- [ ] Backend health check works ✓
- [ ] Environment variables set ✓
- [ ] Frontend updated with backend URL ✓
- [ ] Frontend deployed to Netlify ✓
- [ ] End-to-end test passed ✓
- [ ] Both URLs accessible from phone/other device ✓

---

## 🎬 READY FOR DEMO!

Once deployed:
1. ✅ Share Netlify URL with anyone
2. ✅ Works on any device (phone, tablet, PC)
3. ✅ Record your demo video using the live URL
4. ✅ Submit to competition!

**Your app is now LIVE and accessible worldwide! 🌍🚀**

---

## 🆘 Need Help?

**Railway Issues:**
- Check: https://railway.app/help
- Or Railway Discord: https://discord.gg/railway

**Deployment Questions:**
- Check Railway logs for errors
- Verify all environment variables
- Test backend health endpoint first

---

## 🎉 CONGRATULATIONS!

You've deployed a production-ready AI application! 

**Stack:**
- ⚡ FastAPI backend on Railway
- 🌐 Static frontend on Netlify
- 🤖 OpenAI GPT-4 integration
- 📊 Real government data
- 🔐 Secure HTTPS
- 🌍 Global CDN delivery

**This is enterprise-grade deployment! You should be proud! 🏆**
