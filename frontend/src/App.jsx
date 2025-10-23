import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import DataExplorer from './components/DataExplorer'
import About from './components/About'

function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-green-500 to-blue-500 p-2 rounded-lg">
                <span className="text-white text-2xl">🌾</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-600 to-blue-600">
                  Project Samarth
                </h1>
                <p className="text-sm text-gray-600">
                  Agricultural & Climate Data Intelligence
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <a
                href="https://data.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 hover:text-green-600 transition-colors"
              >
                Powered by data.gov.in
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('chat')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'chat'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <span>💬</span>
                <span>Ask Questions</span>
              </div>
            </button>
            
            <button
              onClick={() => setActiveTab('data')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'data'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <span>📊</span>
                <span>Explore Data</span>
              </div>
            </button>
            
            <button
              onClick={() => setActiveTab('about')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'about'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <span>ℹ️</span>
                <span>About</span>
              </div>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'data' && <DataExplorer />}
        {activeTab === 'about' && <About />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>
              Built for better data-driven agricultural policy making |{' '}
              <span className="text-green-600 font-semibold">
                Government of India Open Data Initiative
              </span>
            </p>
            <p className="mt-2 text-xs text-gray-500">
              Data sources: Ministry of Agriculture & Farmers Welfare | India Meteorological Department
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
