#!/bin/bash

# 🚀 SUPER SIMPLE DEPLOY - Just follow these steps!

echo "=========================================="
echo "🚀 PROJECT SAMARTH - DEPLOY INSTRUCTIONS"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}I'll build your frontend right now!${NC}"
echo ""

cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend

echo -e "${BLUE}Building production version...${NC}"
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build Complete!${NC}"
    echo ""
    echo "=========================================="
    echo -e "${GREEN}🎉 READY TO DEPLOY!${NC}"
    echo "=========================================="
    echo ""
    echo -e "${YELLOW}Your deployment files are in:${NC}"
    echo "  /Users/mayursantoshtarate/Desktop/Apperentice/frontend/dist"
    echo ""
    echo -e "${BLUE}OPTION 1 - Netlify Drop (EASIEST - 2 minutes):${NC}"
    echo ""
    echo "  1. Open this URL in your browser:"
    echo -e "     ${GREEN}https://app.netlify.com/drop${NC}"
    echo ""
    echo "  2. Drag the 'dist' folder onto the page"
    echo "     Location: /Users/mayursantoshtarate/Desktop/Apperentice/frontend/dist"
    echo ""
    echo "  3. Wait 30 seconds"
    echo ""
    echo "  4. You'll get a URL like: https://random-name.netlify.app"
    echo ""
    echo -e "${BLUE}OPTION 2 - Vercel CLI (also easy):${NC}"
    echo ""
    echo "  npm install -g vercel"
    echo "  cd /Users/mayursantoshtarate/Desktop/Apperentice/frontend"
    echo "  vercel --prod"
    echo ""
    echo -e "${RED}⚠️  IMPORTANT NOTE:${NC}"
    echo "  The deployed app will connect to http://localhost:8000"
    echo "  This means it will ONLY work when:"
    echo "  - You access it from the SAME computer"
    echo "  - Your backend is running"
    echo ""
    echo -e "${YELLOW}For TRUE remote access from any device:${NC}"
    echo "  You need to expose your backend with ngrok first."
    echo "  Run: ./expose-backend.sh"
    echo ""
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# Open Finder to the dist folder
echo -e "${BLUE}Opening dist folder in Finder...${NC}"
open /Users/mayursantoshtarate/Desktop/Apperentice/frontend/dist

echo ""
echo -e "${GREEN}Ready to drag & drop! 🚀${NC}"
echo ""
