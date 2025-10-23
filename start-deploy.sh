#!/bin/bash

# 🚀 ONE-COMMAND DEPLOYMENT SETUP
# This will get you deployed in 5 minutes!

echo "=========================================="
echo "🚀 PROJECT SAMARTH - INSTANT DEPLOY"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}This script will:${NC}"
echo "1. ✅ Install ngrok (to expose your backend)"
echo "2. ✅ Give you a public URL for your backend"
echo "3. ✅ Build your frontend for production"
echo "4. ✅ Prepare everything for Netlify deployment"
echo ""
read -p "Ready to proceed? (y/n): " proceed

if [ "$proceed" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}Step 1: Installing ngrok...${NC}"
if ! command -v ngrok &> /dev/null; then
    brew install ngrok
    echo -e "${GREEN}✅ Ngrok installed!${NC}"
else
    echo -e "${GREEN}✅ Ngrok already installed!${NC}"
fi

echo ""
echo -e "${BLUE}Step 2: Checking backend...${NC}"
BACKEND_STATUS=$(curl -s http://localhost:8000/api/v1/health)
if [[ $BACKEND_STATUS == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend is running!${NC}"
else
    echo -e "${RED}❌ Backend not running!${NC}"
    echo ""
    echo "Please start backend first in another terminal:"
    echo -e "${YELLOW}  cd /Users/mayursantoshtarate/Desktop/Apperentice/backend${NC}"
    echo -e "${YELLOW}  source venv/bin/activate${NC}"
    echo -e "${YELLOW}  uvicorn app.main:app --host 0.0.0.0 --port 8000${NC}"
    echo ""
    exit 1
fi

echo ""
echo -e "${BLUE}Step 3: Starting ngrok...${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Keep this window open!${NC}"
echo ""

# Start ngrok in background and capture the URL
ngrok http 8000 > /dev/null &
NGROK_PID=$!

echo "Waiting for ngrok to start..."
sleep 3

# Get the ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok-free\.app')

if [ -z "$NGROK_URL" ]; then
    echo -e "${RED}❌ Failed to get ngrok URL${NC}"
    echo "Please start ngrok manually:"
    echo "  ngrok http 8000"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Backend is now public at:${NC}"
echo -e "${BLUE}   $NGROK_URL${NC}"
echo ""

API_URL="${NGROK_URL}/api/v1"

echo -e "${BLUE}Step 4: Updating frontend API URL...${NC}"

# Update the API URL in api.js
cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend

# Create backup
cp src/services/api.js src/services/api.js.backup

# Update the URL
sed -i '' "s|const API_BASE_URL = 'http://localhost:8000/api/v1'|const API_BASE_URL = '${API_URL}'|g" src/services/api.js

echo -e "${GREEN}✅ API URL updated!${NC}"

echo ""
echo -e "${BLUE}Step 5: Building production version...${NC}"
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    # Restore backup
    mv src/services/api.js.backup src/services/api.js
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 READY TO DEPLOY!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Your backend is exposed at:${NC}"
echo "  $NGROK_URL"
echo ""
echo -e "${BLUE}Your frontend is built in:${NC}"
echo "  frontend/dist/"
echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo ""
echo "OPTION 1 - Netlify Drop (Easiest):"
echo "  1. Open: https://app.netlify.com/drop"
echo "  2. Drag the 'dist' folder onto the page"
echo "  3. Wait 30 seconds"
echo "  4. Done! You get a public URL!"
echo ""
echo "OPTION 2 - Netlify CLI:"
echo "  npm install -g netlify-cli"
echo "  cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend"
echo "  netlify deploy --prod --dir=dist"
echo ""
echo -e "${RED}⚠️  IMPORTANT:${NC}"
echo "  Keep this terminal window open!"
echo "  Ngrok must stay running for your deployed app to work!"
echo "  (Press Ctrl+C when you're done testing)"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
echo ""

# Keep ngrok running
wait $NGROK_PID
