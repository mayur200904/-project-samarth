#!/bin/bash

# Project Samarth - Complete Setup and Test Script
# This script sets up and tests your entire application

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🌾 Project Samarth - Setup & Test Script 🌾          ║"
echo "║    Intelligent Agricultural & Climate Data Q&A System        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Check if running from project root
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "Project root detected: $(pwd)"
echo ""

# Step 1: Check Python
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Checking Python installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"
echo ""

# Step 2: Check Node.js
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Checking Node.js installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js $NODE_VERSION found"
echo ""

# Step 3: Configure environment
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Configuring environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend

if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    
    # Check if user wants to configure now
    echo ""
    echo "You need to configure your LLM provider. Options:"
    echo "  1) OpenAI (recommended, requires API key)"
    echo "  2) Ollama (local, no API key, requires Ollama installation)"
    echo "  3) Skip for now (you can configure manually later)"
    echo ""
    read -p "Choose option (1/2/3): " llm_choice
    
    case $llm_choice in
        1)
            read -p "Enter your OpenAI API key: " openai_key
            cat > .env << EOF
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=$openai_key
MODEL_NAME=gpt-4-turbo-preview

# Other settings (defaults)
DEBUG=true
LOG_LEVEL=info
DATA_DIRECTORY=./data
CHROMA_PERSIST_DIRECTORY=./chroma_db
CACHE_TTL=86400
EOF
            print_success ".env file created with OpenAI configuration"
            ;;
        2)
            cat > .env << EOF
# LLM Configuration  
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Other settings (defaults)
DEBUG=true
LOG_LEVEL=info
DATA_DIRECTORY=./data
CHROMA_PERSIST_DIRECTORY=./chroma_db
CACHE_TTL=86400
EOF
            print_success ".env file created with Ollama configuration"
            print_warning "Make sure Ollama is installed and running!"
            print_info "Install: curl -fsSL https://ollama.ai/install.sh | sh"
            print_info "Pull model: ollama pull llama3.1"
            ;;
        3)
            cp .env .env 2>/dev/null || echo "# Configure me!" > .env
            print_warning ".env created but needs manual configuration"
            print_info "Edit backend/.env and add your API key before running"
            ;;
    esac
else
    print_success ".env file already exists"
fi

echo ""

# Step 4: Backend dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Installing backend dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

print_info "Activating virtual environment..."
source venv/bin/activate

print_info "Installing Python packages (this may take a few minutes)..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

print_success "Backend dependencies installed"
echo ""

# Step 5: Frontend dependencies
cd ..
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Installing frontend dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd frontend
print_info "Installing npm packages (this may take a few minutes)..."
npm install --silent

print_success "Frontend dependencies installed"
echo ""

# Step 6: Test backend
cd ..
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Testing backend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend
source venv/bin/activate

print_info "Starting backend server in background..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

print_info "Waiting for backend to start..."
sleep 10

# Test health endpoint
print_info "Testing health endpoint..."
if curl -s http://localhost:8000/api/v1/health | grep -q "healthy"; then
    print_success "Backend is running and healthy!"
else
    print_error "Backend health check failed"
    print_info "Check backend.log for errors"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Test datasets endpoint
print_info "Testing datasets endpoint..."
if curl -s http://localhost:8000/api/v1/datasets | grep -q "crop_production"; then
    print_success "Datasets API is working!"
else
    print_warning "Datasets API returned unexpected response"
fi

echo ""

# Step 7: Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Setup Complete! ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_success "Backend is running on http://localhost:8000"
print_info "Backend PID: $BACKEND_PID"
print_info "Logs: backend/backend.log"
echo ""
print_info "To start the frontend, open a NEW terminal and run:"
echo ""
echo "  cd frontend"
echo "  npm run dev"
echo ""
print_info "Then open http://localhost:5173 in your browser"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Start frontend: cd frontend && npm run dev"
echo "2. Open browser: http://localhost:5173"
echo "3. Try sample questions in the chat"
echo "4. Explore datasets in the Data Explorer tab"
echo "5. Read docs/VIDEO_SCRIPT.md for demo guidance"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 To stop the backend:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  kill $BACKEND_PID"
echo ""
echo "Or press Ctrl+C in the terminal running the frontend"
echo ""
print_success "Happy querying! 🌾"
echo ""
