# Create .env file from example
cp .env.example .env

echo "📝 Please edit .env file and add your API keys:"
echo "   - OPENAI_API_KEY (or ANTHROPIC_API_KEY or GOOGLE_API_KEY)"
echo "   - DATA_GOV_API_KEY (optional but recommended)"
echo ""
echo "For local deployment without external APIs, set:"
echo "   LLM_PROVIDER=ollama"
echo ""
read -p "Press enter when you've configured .env..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

echo "✅ Frontend setup complete!"
echo ""
echo "🚀 Setup complete! To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
