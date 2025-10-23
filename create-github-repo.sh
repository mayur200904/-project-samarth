#!/bin/bash

# 🚀 Create GitHub Repository - Simple Method

echo "=========================================="
echo "📦 CREATE GITHUB REPOSITORY"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Option 1: Using GitHub Website (Easiest!)${NC}"
echo ""
echo "1. Go to: https://github.com/new"
echo ""
echo "2. Fill in:"
echo "   Repository name: project-samarth"
echo "   Description: Intelligent Q&A System for Indian Agricultural & Climate Data"
echo "   Visibility: Public"
echo "   ✓ Do NOT initialize with README (we already have one)"
echo ""
echo "3. Click 'Create repository'"
echo ""
echo "4. Copy the commands shown and run them:"
echo ""
echo -e "${YELLOW}Run these commands:${NC}"
echo ""
echo "cd /Users/mayursantoshtarate/Desktop/Apperentice"
echo "git remote add origin https://github.com/YOUR_USERNAME/project-samarth.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "=========================================="
echo ""
echo -e "${BLUE}Option 2: Using GitHub CLI${NC}"
echo ""
echo "1. Authenticate with GitHub:"
echo "   gh auth login"
echo "   (Follow the prompts, use web browser)"
echo ""
echo "2. Create and push repo:"
echo "   cd /Users/mayursantoshtarate/Desktop/Apperentice"
echo "   gh repo create project-samarth --public --source=. --remote=origin --push"
echo ""
echo "=========================================="
echo ""
echo -e "${GREEN}After creating the repo, you can use it for Railway deployment!${NC}"
echo ""
