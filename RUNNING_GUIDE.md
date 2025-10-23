# 🚀 Project Samarth - Running Guide

## ✅ Current Status: **SYSTEM IS LIVE!**

### Backend Status
- **URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/v1/health
- **Status**: ✅ Healthy
- **Uptime**: Running
- **Loaded Datasets**: 6,820 data points

### Frontend Status
- **URL**: http://localhost:5173
- **Status**: ✅ Running
- **Vite Dev Server**: Active

---

## 🎯 How to Use the Application

### 1. Open the Application
The application should already be open in your browser at:
**http://localhost:5173**

If not, open it manually in your browser.

### 2. Navigate Through Tabs

#### 🤖 **Chat Tab** (Main Feature)
- This is your intelligent Q&A interface
- Try these sample questions:
  1. **"Compare rice production in Punjab and West Bengal"**
  2. **"Which state had highest rainfall in 2020?"**
  3. **"Show me wheat production trends over the last 5 years"**
  4. **"What are the agricultural prices for cotton?"**

**Features:**
- ✅ Natural language questions
- ✅ AI-powered answers with citations
- ✅ Source links to verify data
- ✅ Export conversation to Markdown
- ✅ Copy responses to clipboard
- ✅ Processing time display

#### 📊 **Data Explorer Tab**
- Browse all 5 available datasets
- Filter by category (agriculture/climate)
- Search by name or description
- Refresh datasets
- View dataset metadata

#### ℹ️ **About Tab**
- System features and capabilities
- Architecture overview
- Technical highlights
- Performance metrics

---

## 🧪 Testing Checklist

### Step 1: Test Backend Health
```bash
curl http://localhost:8000/api/v1/health | python3 -m json.tool
```
Expected: Status "healthy" with all services operational

### Step 2: Test Chat Interface
1. Go to Chat tab
2. Click any sample question OR type your own
3. Verify:
   - ✅ Response appears in ~5-10 seconds
   - ✅ Citations show source datasets
   - ✅ Links are clickable
   - ✅ Response is relevant and accurate

### Step 3: Test Data Explorer
1. Go to Data Explorer tab
2. Verify all 5 datasets appear
3. Try filtering by "Agriculture" category
4. Search for "rainfall"
5. Click "Refresh" on any dataset

### Step 4: Export Functionality
1. Ask 2-3 questions in Chat
2. Click "Export Conversation" button
3. Verify Markdown file downloads
4. Try "Copy to Clipboard" button

---

## 🎬 Recording Your Demo Video

### Before Recording:
1. ✅ Backend running at http://localhost:8000
2. ✅ Frontend running at http://localhost:5173
3. ✅ Browser window maximized
4. ✅ Close unnecessary tabs
5. ✅ Clear browser console errors (F12)

### Recording Script (2 minutes)
Follow the detailed script in: **`docs/VIDEO_SCRIPT.md`**

**Quick Timeline:**
- **[0:00-0:15]** Introduction - Problem statement
- **[0:15-0:45]** Live demo - Ask 2 questions
- **[0:45-1:15]** Architecture - Show system design
- **[1:15-1:45]** Differentiators - Key features
- **[1:45-2:00]** Impact & wrap-up

**Pro Tips:**
- Practice 2-3 times before final recording
- Speak clearly and confidently
- Show actual queries and responses
- Highlight source citations
- Keep energy high!

---

## 🛠️ If Something Goes Wrong

### Backend Not Responding?
```bash
# Check if backend is running
ps aux | grep uvicorn

# If not, restart:
cd /Users/mayursantoshtarate/Desktop/Apperentice/backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

### Frontend Not Loading?
```bash
# Check if Vite is running
ps aux | grep vite

# If not, restart:
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
npx vite
```

### Chat Not Working?
1. Check browser console (F12) for errors
2. Verify backend health: http://localhost:8000/api/v1/health
3. Check OpenAI API key in `backend/.env`
4. Look at backend logs: `tail -f backend/backend.log`

### Data Not Loading?
1. Check backend logs for errors
2. Verify datasets in Data Explorer tab
3. Backend will use sample data if API fails (this is normal!)

---

## 📝 Next Steps for Submission

### 1. Test Everything (30 minutes)
- [ ] Test all 4 sample questions
- [ ] Test custom questions
- [ ] Verify all citations work
- [ ] Check Data Explorer loads
- [ ] Test export functionality
- [ ] Verify no errors in console

### 2. Record Video (1 hour)
- [ ] Practice demo 2-3 times
- [ ] Record with Loom (<2 minutes)
- [ ] Upload to Loom
- [ ] Get shareable link
- [ ] Test the link works

### 3. Final Verification
- [ ] Complete `SUBMISSION_CHECKLIST.md`
- [ ] Ensure `.env` not in git
- [ ] Push code to GitHub (if required)
- [ ] Prepare submission package

### 4. Submit! 🎉
- [ ] Video link
- [ ] GitHub repository (if required)
- [ ] Documentation
- [ ] Any additional materials

---

## 🏆 Your Competitive Advantages

1. **Production-Ready Architecture** - Not just a demo
2. **Multi-LLM Support** - Flexible provider switching
3. **Real Data Integration** - data.gov.in API + smart caching
4. **Source Citations** - Full transparency and verifiability
5. **Modern UX** - Beautiful React interface with TailwindCSS
6. **Complete Documentation** - Everything evaluators need
7. **Advanced RAG** - Semantic search with vector embeddings
8. **6,820+ Data Points** - Comprehensive agricultural datasets

---

## 📞 Quick Reference

### URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Key Files
- **Configuration**: `backend/.env`
- **Backend Logs**: `backend/backend.log`
- **Video Script**: `docs/VIDEO_SCRIPT.md`
- **Submission Checklist**: `SUBMISSION_CHECKLIST.md`

### Commands
```bash
# Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend
cd frontend && npx vite

# Health Check
curl http://localhost:8000/api/v1/health
```

---

## 🎉 You're Ready!

Your Project Samarth system is **LIVE and RUNNING**! 

Test it thoroughly, record your amazing demo, and submit with confidence!

**Good luck with your submission! 🚀**
