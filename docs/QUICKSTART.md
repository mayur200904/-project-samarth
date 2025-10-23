# 🚀 Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- API Key (OpenAI/Anthropic/Google) OR Ollama for local deployment

## Installation

### Option 1: Automated Setup (Recommended)

```bash
cd /Users/mayursantoshtarate/Desktop/Apperentice
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API key
```

Minimum configuration needed in `.env`:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

For local deployment without external APIs:
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
```

#### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
.\venv\Scripts\activate  # On Windows

pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     🚀 Starting Project Samarth Backend...
INFO:     ✅ Data fetcher initialized
INFO:     ✅ RAG service initialized
INFO:     📊 Loading initial datasets...
INFO:     ✅ Initial datasets loaded
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 500 ms
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## First Steps

### 1. Verify Backend is Running

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 10.5,
  "services": {
    "api": "healthy",
    "rag": "healthy",
    "data_fetcher": "healthy"
  }
}
```

### 2. Check Available Datasets

```bash
curl http://localhost:8000/api/v1/datasets
```

### 3. Ask Your First Question

Via API:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Compare rice production in Punjab and West Bengal"
  }'
```

Via UI:
1. Open http://localhost:5173
2. Click on a sample question or type your own
3. Hit Send!

## Sample Questions to Try

1. **Comparison**:
   ```
   Compare rice production in Punjab and West Bengal over the last 5 years
   ```

2. **Trend Analysis**:
   ```
   Analyze sugarcane production trend in Uttar Pradesh over the last decade
   ```

3. **District Level**:
   ```
   Which district in Maharashtra has the highest wheat production?
   ```

4. **Climate Correlation**:
   ```
   How does rainfall affect rice production in West Bengal?
   ```

5. **Policy Recommendation**:
   ```
   What are 3 data-backed arguments for promoting millets in drought-prone regions?
   ```

## Troubleshooting

### Backend won't start

**Error**: `Import "app.core.config" could not be resolved`
```bash
# Make sure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate
python -c "import app.core.config"  # Test import
```

**Error**: `OpenAI API key not set`
```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY
# Or use Ollama instead
```

### Frontend won't connect to backend

**Error**: `Network Error` or `Failed to fetch`

1. Check backend is running: `curl http://localhost:8000/api/v1/health`
2. Check CORS settings in `backend/app/core/config.py`
3. Clear browser cache

### Slow responses

**Issue**: Queries take > 30 seconds

Possible causes:
1. First query is slow (loading datasets) - subsequent queries are faster
2. LLM API is slow - consider using a faster model or local Ollama
3. Large datasets - check `MAX_DATASET_SIZE_MB` in config

### No data returned

**Issue**: "No datasets found"

```bash
# Force refresh datasets
cd backend
source venv/bin/activate
python -c "
from app.services.data_fetcher import DataFetcher
import asyncio
async def refresh():
    df = DataFetcher()
    await df.load_initial_datasets()
asyncio.run(refresh())
"
```

## Using Local LLM (Ollama)

For completely offline/private deployment:

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai
```

### 2. Pull a Model

```bash
ollama pull llama3.1
```

### 3. Configure Project Samarth

Edit `.env`:
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

### 4. Restart Backend

The system will now use your local LLM - no external API calls!

## Next Steps

- 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- 🔧 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 🧪 Run tests: `cd backend && pytest`
- 📊 Explore the Data Explorer tab to see available datasets
- 🎨 Customize the UI in `frontend/src/components/`

## Getting Help

1. Check the logs:
   - Backend: In the terminal running uvicorn
   - Frontend: Browser DevTools Console (F12)

2. Verify configuration:
   ```bash
   # Backend
   cd backend && python -c "from app.core.config import settings; print(settings)"
   
   # Frontend
   # Check browser console for API_BASE_URL
   ```

3. Common issues:
   - API key not set → Edit `.env`
   - Port already in use → Change port or kill process
   - Module not found → Reinstall dependencies

---

**🎉 You're all set! Happy querying!**
