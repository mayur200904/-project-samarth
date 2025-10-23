#!/bin/bash

# 🚀 Complete Railway Deployment Script
# For GitHub Student Developer Pack users!

echo "=========================================="
echo "🚀 PROJECT SAMARTH - RAILWAY DEPLOYMENT"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

cd /Users/mayursantoshtarate/Desktop/Apperentice

echo -e "${BLUE}Creating deployment-ready files...${NC}"
echo ""

# Create standalone simple.html that works anywhere
cat > frontend/standalone-simple.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Samarth - Q&A System</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-green-50 to-blue-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <div class="bg-white rounded-2xl shadow-xl p-8">
            <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-green-600 mb-2">🌾 Project Samarth</h1>
                <p class="text-gray-600">Intelligent Q&A System for Indian Agricultural & Climate Data</p>
            </div>

            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">Ask Your Question</label>
                <div class="flex gap-2">
                    <input 
                        type="text" 
                        id="questionInput"
                        placeholder="E.g., Compare rice production in Punjab and West Bengal"
                        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <button 
                        onclick="askQuestion()"
                        id="askButton"
                        class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                    >
                        Ask
                    </button>
                </div>
            </div>

            <div class="mb-6">
                <p class="text-sm text-gray-600 mb-2">Try these sample questions:</p>
                <div class="flex flex-wrap gap-2">
                    <button onclick="useSample(this)" class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200">
                        Compare rice production in Punjab and West Bengal
                    </button>
                    <button onclick="useSample(this)" class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200">
                        What are the rainfall patterns in Maharashtra?
                    </button>
                    <button onclick="useSample(this)" class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200">
                        Show me wheat production trends
                    </button>
                </div>
            </div>

            <div id="loadingDiv" class="hidden text-center py-8">
                <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
                <p class="mt-4 text-gray-600">Processing your question... (this takes ~25 seconds)</p>
            </div>

            <div id="answerDiv" class="hidden">
                <h3 class="text-lg font-semibold text-gray-800 mb-3">Answer:</h3>
                <div id="answerText" class="prose max-w-none bg-gray-50 p-4 rounded-lg mb-4"></div>
                
                <div id="citationsDiv" class="hidden">
                    <h4 class="text-md font-semibold text-gray-700 mb-2">Sources:</h4>
                    <div id="citationsList" class="space-y-2"></div>
                </div>
            </div>

            <div id="errorDiv" class="hidden bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-red-700" id="errorText"></p>
            </div>
        </div>

        <div class="text-center mt-6 text-sm text-gray-600">
            <p>Powered by GPT-4 • 5 Government Datasets • 6,820+ Records</p>
        </div>
    </div>

    <script>
        // CHANGE THIS to your Railway backend URL after deployment
        const API_URL = 'REPLACE_WITH_YOUR_RAILWAY_BACKEND_URL/api/v1';

        function useSample(button) {
            document.getElementById('questionInput').value = button.textContent.trim();
        }

        async function askQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            
            if (!question) {
                alert('Please enter a question');
                return;
            }

            document.getElementById('loadingDiv').classList.remove('hidden');
            document.getElementById('answerDiv').classList.add('hidden');
            document.getElementById('errorDiv').classList.add('hidden');
            document.getElementById('askButton').disabled = true;
            document.getElementById('askButton').textContent = 'Processing...';

            try {
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: question })
                });

                if (!response.ok) {
                    throw new Error('Failed to get response from backend');
                }

                const data = await response.json();

                document.getElementById('loadingDiv').classList.add('hidden');
                document.getElementById('answerDiv').classList.remove('hidden');
                document.getElementById('answerText').innerHTML = data.answer.replace(/\n/g, '<br>');

                if (data.citations && data.citations.length > 0) {
                    document.getElementById('citationsDiv').classList.remove('hidden');
                    const citationsList = document.getElementById('citationsList');
                    citationsList.innerHTML = data.citations.map((citation, i) => `
                        <div class="bg-blue-50 p-3 rounded">
                            <p class="text-sm text-blue-900">
                                <strong>[${i + 1}]</strong> ${citation.source || 'Government Dataset'}
                            </p>
                        </div>
                    `).join('');
                }

            } catch (error) {
                document.getElementById('loadingDiv').classList.add('hidden');
                document.getElementById('errorDiv').classList.remove('hidden');
                document.getElementById('errorText').textContent = 'Error: ' + error.message;
            } finally {
                document.getElementById('askButton').disabled = false;
                document.getElementById('askButton').textContent = 'Ask';
            }
        }

        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    </script>
</body>
</html>
HTMLEOF

echo -e "${GREEN}✅ Created standalone-simple.html${NC}"

# Create Railway config for backend
cat > backend/railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

cat > backend/Procfile << 'EOF'
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF

cat > backend/runtime.txt << 'EOF'
python-3.11
EOF

echo -e "${GREEN}✅ Created Railway configuration files${NC}"

# Update .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
.env
backend/.env
node_modules/
frontend/dist/
.DS_Store
chroma_db/
data/*.parquet
EOF

echo -e "${GREEN}✅ Created .gitignore${NC}"

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit - Project Samarth"
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 FILES READY!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Created:${NC}"
echo "  ✅ frontend/standalone-simple.html (your UI)"
echo "  ✅ backend/railway.json (deployment config)"
echo "  ✅ backend/Procfile"
echo "  ✅ backend/runtime.txt"
echo "  ✅ .gitignore"
echo ""
echo -e "${YELLOW}See RAILWAY_DEPLOY.md for complete step-by-step instructions!${NC}"
echo ""
