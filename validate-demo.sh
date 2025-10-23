#!/bin/bash

# 🎬 Pre-Recording Validation Script
# Run this before recording your demo video!

echo "=========================================="
echo "🎬 PROJECT SAMARTH - DEMO READINESS CHECK"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: Backend Health
echo "1️⃣  Checking Backend Health..."
BACKEND_HEALTH=$(curl -s http://localhost:8000/api/v1/health)
if [[ $BACKEND_HEALTH == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend is running and healthy!${NC}"
else
    echo -e "${RED}❌ Backend not responding! Start it first:${NC}"
    echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    exit 1
fi
echo ""

# Check 2: Frontend Accessible
echo "2️⃣  Checking Frontend..."
FRONTEND_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/simple.html)
if [ "$FRONTEND_CHECK" == "200" ]; then
    echo -e "${GREEN}✅ Frontend (simple.html) is accessible!${NC}"
else
    echo -e "${RED}❌ Frontend not responding! Start it first:${NC}"
    echo "   cd frontend && npx vite"
    exit 1
fi
echo ""

# Check 3: Test Query
echo "3️⃣  Testing Sample Query..."
TEST_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Test query"}' \
  | grep -o '"answer"' | wc -l)

if [ "$TEST_RESPONSE" -ge 1 ]; then
    echo -e "${GREEN}✅ Backend can answer questions!${NC}"
else
    echo -e "${RED}❌ Backend not responding to queries!${NC}"
    exit 1
fi
echo ""

# Check 4: Environment Variables
echo "4️⃣  Checking Environment..."
if [ -f "backend/.env" ]; then
    if grep -q "OPENAI_API_KEY" backend/.env; then
        echo -e "${GREEN}✅ OpenAI API key configured!${NC}"
    else
        echo -e "${YELLOW}⚠️  OpenAI API key might be missing${NC}"
    fi
else
    echo -e "${RED}❌ backend/.env file missing!${NC}"
    exit 1
fi
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}🎉 ALL SYSTEMS READY FOR DEMO!${NC}"
echo "=========================================="
echo ""
echo "📋 NEXT STEPS:"
echo "1. Open http://localhost:5173/simple.html in browser"
echo "2. Have sample questions ready to paste"
echo "3. Start Loom recording"
echo "4. Follow DEMO_CHECKLIST.md script"
echo ""
echo "🎬 Sample Questions:"
echo "   • Compare rice production in Punjab and West Bengal"
echo "   • What are the rainfall patterns in Maharashtra?"
echo "   • Show me wheat production trends over the years"
echo ""
echo -e "${GREEN}Good luck! You've got this! 🚀${NC}"
echo ""
