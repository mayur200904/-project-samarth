#!/bin/bash

# 🚀 Quick Deploy Script for Project Samarth
# This creates a standalone simple.html that can be deployed anywhere

echo "=========================================="
echo "🚀 PROJECT SAMARTH - QUICK DEPLOY"
echo "=========================================="
echo ""

cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📦 Step 1: Creating standalone deployment package...${NC}"

# Create deploy directory
mkdir -p deploy

# Copy simple.html to deploy folder
cp simple.html deploy/index.html

echo -e "${GREEN}✅ Created deploy/index.html${NC}"
echo ""

# Get user's choice for backend
echo -e "${YELLOW}Where is your backend?${NC}"
echo "1) Local (http://localhost:8000)"
echo "2) I'll expose it with ngrok"
echo "3) Already deployed (I have a URL)"
echo ""
read -p "Choose (1-3): " backend_choice

case $backend_choice in
    1)
        BACKEND_URL="http://localhost:8000/api/v1"
        echo -e "${YELLOW}⚠️  Note: Local backend only works on your computer${NC}"
        ;;
    2)
        echo ""
        echo -e "${BLUE}Starting ngrok...${NC}"
        if ! command -v ngrok &> /dev/null; then
            echo -e "${YELLOW}Installing ngrok...${NC}"
            brew install ngrok
        fi
        
        echo ""
        echo -e "${YELLOW}In another terminal, run:${NC}"
        echo -e "${BLUE}  ngrok http 8000${NC}"
        echo ""
        read -p "Enter your ngrok URL (e.g., https://abc123.ngrok.io): " ngrok_url
        BACKEND_URL="${ngrok_url}/api/v1"
        ;;
    3)
        read -p "Enter your backend URL (e.g., https://api.example.com/api/v1): " custom_url
        BACKEND_URL="$custom_url"
        ;;
    *)
        BACKEND_URL="http://localhost:8000/api/v1"
        ;;
esac

echo ""
echo -e "${BLUE}📝 Step 2: Updating API URL to: ${BACKEND_URL}${NC}"

# Update the API URL in the HTML file
sed -i '' "s|http://localhost:8000/api/v1|${BACKEND_URL}|g" deploy/index.html

echo -e "${GREEN}✅ API URL updated${NC}"
echo ""

echo -e "${BLUE}📦 Step 3: Creating deployment package...${NC}"

# Create a simple README for the deploy folder
cat > deploy/README.txt << 'EOF'
PROJECT SAMARTH - DEPLOYMENT PACKAGE
=====================================

This folder contains everything needed to deploy the frontend.

OPTION 1: Netlify Drop (Easiest)
---------------------------------
1. Go to: https://app.netlify.com/drop
2. Drag this entire 'deploy' folder onto the page
3. Done! You'll get a URL instantly

OPTION 2: Vercel
----------------
1. Install: npm install -g vercel
2. Run: vercel deploy
3. Done!

OPTION 3: Any Web Server
-------------------------
Just upload index.html to any web hosting service.

The app will work as long as your backend is accessible!
EOF

echo -e "${GREEN}✅ Deployment package ready!${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}🎉 SUCCESS! Ready to Deploy!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Your deployment files are in:${NC}"
echo "  frontend/deploy/"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo -e "${YELLOW}FASTEST METHOD (Netlify Drop):${NC}"
echo "  1. Open: https://app.netlify.com/drop"
echo "  2. Drag the 'deploy' folder onto the page"
echo "  3. Get instant URL!"
echo ""
echo -e "${YELLOW}OR use Vercel:${NC}"
echo "  cd frontend/deploy"
echo "  npx vercel --prod"
echo ""
echo -e "${BLUE}Backend URL configured:${NC} ${BACKEND_URL}"
echo ""
echo -e "${GREEN}You can now access your Q&A system from anywhere! 🚀${NC}"
echo ""
