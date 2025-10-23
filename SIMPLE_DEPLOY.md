# 🚀 SUPER SIMPLE DEPLOYMENT - 5 MINUTES!

## Option 1: Deploy with Netlify (EASIEST - Drag & Drop!) ⭐

### Step 1: Prepare Backend Access

**Choose ONE:**

#### A. Use Ngrok (Expose Local Backend)
```bash
# Install ngrok
brew install ngrok

# In a terminal, run:
cd /Users/mayursantoshtarate/Desktop/Apperentice/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In ANOTHER terminal, run:
ngrok http 8000
```

Copy the URL (e.g., `https://abc123.ngrok-free.app`) ✅

#### B. Deploy Backend First (Skip if using ngrok)
Deploy backend to Railway/Render first, then come back.

---

### Step 2: Update Frontend API URL

```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
```

Edit `src/services/api.js` - change line 4:
```javascript
// FROM:
const API_BASE_URL = 'http://localhost:8000/api/v1'

// TO:
const API_BASE_URL = 'https://your-ngrok-url.ngrok-free.app/api/v1'
```

---

### Step 3: Build Production Version

```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
npm run build
```

This creates a `dist` folder with everything ready! ✅

---

### Step 4: Deploy to Netlify (2 Minutes!)

#### Method 1: Drag & Drop (No Account Needed!)
1. Go to: **https://app.netlify.com/drop**
2. **Drag the `dist` folder** onto the page
3. Wait 30 seconds
4. **DONE!** You get a URL like `https://random-name-123.netlify.app`

#### Method 2: With CLI (For Custom Domain)
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
netlify deploy --prod --dir=dist
```

Follow prompts:
- Create new site? **Yes**
- Site name: `project-samarth` (or any name you want)

You'll get a URL! ✅

---

## Option 2: Deploy with Vercel (Also Easy!) 🔺

### Step 1-3: Same as above (update API URL and build)

### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend
vercel --prod
```

Follow prompts:
- Setup and deploy: **Yes**
- Scope: Your account
- Link to existing project: **No**
- Project name: `project-samarth`
- Directory: **./dist**
- Override settings: **No**

You'll get a URL! ✅

---

## Complete Commands (Copy-Paste Ready!)

### For Ngrok + Netlify:

```bash
# Terminal 1: Start backend
cd /Users/mayursantoshtarate/Desktop/Apperentice/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start ngrok
ngrok http 8000
# Copy the https URL you get!

# Terminal 3: Update and deploy frontend
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend

# Edit src/services/api.js - replace the API_BASE_URL

# Build
npm run build

# Deploy (choose one):
# Option A: Drag & drop dist folder to https://app.netlify.com/drop
# Option B: Use CLI
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

---

## Testing Your Deployment

After deployment:

1. Open your deployed URL (e.g., `https://project-samarth.netlify.app`)
2. Type: "Compare rice production in Punjab and West Bengal"
3. Click "Ask Question"
4. Wait ~25 seconds
5. See your answer with citations! 🎉

---

## Troubleshooting

### "Failed to process question"
- ✅ Make sure ngrok is running
- ✅ Check API URL in `src/services/api.js` matches your ngrok URL
- ✅ Rebuild: `npm run build`
- ✅ Redeploy

### CORS Errors
Add this to `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Cost

- **Netlify**: FREE ✅
- **Vercel**: FREE ✅
- **Ngrok**: FREE for basic use ✅
- **Total**: $0/month

---

## What You Get

✅ Public URL accessible from anywhere  
✅ HTTPS (secure)  
✅ Fast CDN delivery  
✅ Can share link with anyone  
✅ Perfect for demo/competition  

---

## Next Steps After Deployment

1. ✅ Test your deployed URL
2. ✅ Share link with friends/judges
3. ✅ Record demo video using deployed version
4. ✅ Submit to competition!

**Your Q&A system is now live! 🚀**
