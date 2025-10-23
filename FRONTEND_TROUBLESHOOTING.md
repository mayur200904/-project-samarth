# 🔧 Frontend Troubleshooting Guide

## Current Status
- ✅ Backend: Working perfectly (tested and verified)
- ⚠️  Frontend: Not displaying responses (white screen issue)

---

## Quick Fix Steps

### Step 1: Test API Connection (FIRST!)

Open this URL in your browser:
```
http://localhost:5173/test-api.html
```

**Click both buttons:**
1. "Test Health Endpoint" - Should show ✅ success
2. "Test Chat Endpoint" - Should show ✅ response after ~25 seconds

**If both work:** API connection is fine, issue is in React app
**If they fail:** CORS or network issue

---

### Step 2: Check Browser Console

1. Open the main app: `http://localhost:5173`
2. Press **F12** or **Cmd+Option+I** (Mac) to open DevTools
3. Go to **Console** tab
4. Look for RED error messages

**Common errors to look for:**
- ❌ `CORS policy` - Backend CORS issue
- ❌ `Failed to fetch` - API URL wrong
- ❌ `Cannot read property` - React component error
- ❌ `Module not found` - Missing dependency

**Copy any errors you see!**

---

### Step 3: Check Network Tab

1. Keep DevTools open
2. Go to **Network** tab
3. Try asking a question in the chat
4. Look for a request to `/chat`

**What to check:**
- Is the request being made?
- What's the URL? (should be `http://localhost:8000/api/v1/chat`)
- What's the status code?
  - 200 = Success
  - 404 = Wrong URL
  - 500 = Server error
  - Failed/CORS = Connection issue

---

### Step 4: Verify Environment Variable

Open browser console and type:
```javascript
console.log(import.meta.env.VITE_API_URL)
```

**Expected output:** `http://localhost:8000/api/v1`

**If undefined:** Vite didn't load the `.env` file

---

## Manual Fixes

### Fix 1: If API URL is undefined

**Option A - Hardcode the URL (Quick Fix)**

Edit `frontend/src/services/api.js` line 3:

```javascript
// Change this:
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

// To this:
const API_BASE_URL = 'http://localhost:8000/api/v1'
```

Then restart frontend:
```bash
cd frontend
pkill -f vite
npx vite
```

**Option B - Fix the .env file**

Make sure `frontend/.env` exists with:
```
VITE_API_URL=http://localhost:8000/api/v1
```

Then **RESTART** vite (Ctrl+C, then `npx vite`)

---

### Fix 2: If CORS Error

The backend `.env` should have:
```
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

**Check** `backend/.env` line 60-ish.

If wrong, fix it and restart backend:
```bash
cd backend
source venv/bin/activate
pkill -f uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

---

### Fix 3: If React App Not Loading (White Screen)

Check browser console for:
```
Uncaught SyntaxError
```

This means a JavaScript file has an error.

**Quick test:**
```bash
cd frontend
npm run build
```

If build fails, you'll see the exact error.

---

## Verification Checklist

Use this checklist to verify everything:

- [ ] Backend health check works: `curl http://localhost:8000/api/v1/health`
- [ ] Backend chat works: (see BACKEND_TEST_REPORT.md)
- [ ] Frontend Vite server running: `ps aux | grep vite`
- [ ] Frontend loads: Can see title in browser
- [ ] Test API page works: `http://localhost:5173/test-api.html`
- [ ] Main app loads: `http://localhost:5173`
- [ ] No console errors (F12)
- [ ] Can type in chat input
- [ ] Can click "Send"
- [ ] Response appears after ~25s

---

## Still Not Working?

### Debug Mode - Run These Commands:

```bash
# 1. Check backend is running
ps aux | grep uvicorn

# 2. Check frontend is running  
ps aux | grep vite

# 3. Test backend directly
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' | head -20

# 4. Check if frontend can reach backend
curl -s http://localhost:5173/test-api.html | grep "API Connection Test"

# 5. Check for port conflicts
lsof -ti:8000
lsof -ti:5173
```

---

## Alternative: Use cURL Instead of Frontend

If frontend is still problematic, you can demo the backend directly:

```bash
# Save this as ask_question.sh
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"$1\"}" | \
  python3 -c "import sys, json; d=json.load(sys.stdin); print('\n' + d['answer'] + '\n')"

# Usage:
chmod +x ask_question.sh
./ask_question.sh "Compare rice production in Punjab and West Bengal"
```

---

## For Your Demo Video

If frontend still doesn't work in time:

**Option 1:** Show the backend working via cURL (impressive for technical audience)

**Option 2:** Use the test-api.html page (shows the system works)

**Option 3:** Fix just the API connection and skip the fancy UI

Remember: **The backend (brain) is 100% working!** The frontend is just the pretty face.

---

## Next Steps After Fixing

Once you see responses in the frontend:

1. ✅ Test all 4 sample questions
2. ✅ Verify citations appear
3. ✅ Check Data Explorer tab
4. ✅ Test export functionality
5. ✅ Practice your demo
6. ✅ Record video
7. ✅ Submit!

---

*Created: 2025-10-23*
*Backend Status: ✅ FULLY FUNCTIONAL*
*Frontend Status: ⚠️  Under Repair*
