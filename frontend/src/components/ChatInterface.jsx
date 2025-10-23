import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, BookOpen, Download, Copy, CheckCircle2 } from 'lucide-react'
import { askQuestion } from '../services/api'
import ReactMarkdown from 'react-markdown'

const SAMPLE_QUESTIONS = [
  "Compare rice production in Punjab and West Bengal over the last 5 years with rainfall patterns",
  "Which district in Maharashtra has the highest wheat production in 2023?",
  "Analyze the trend of sugarcane production in Uttar Pradesh over the last decade",
  "What are 3 data-backed arguments for promoting millets in water-stressed regions?"
]

function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [copiedIndex, setCopiedIndex] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await askQuestion(input)
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        dataSources: response.data_sources_used,
        confidence: response.confidence,
        processingTime: response.processing_time,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `❌ **Error**: ${error.message}\n\nPlease check:\n- Backend server is running (http://localhost:8000)\n- API key is configured in .env\n- Network connection is stable`,
        isError: true,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSampleQuestion = (question) => {
    setInput(question)
  }

  const copyToClipboard = async (text, index) => {
    await navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const exportConversation = () => {
    const content = messages
      .map(msg => `**${msg.role.toUpperCase()}** (${new Date(msg.timestamp).toLocaleString()}):\n${msg.content}\n\n`)
      .join('\n---\n\n')
    
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `samarth-conversation-${Date.now()}.md`
    a.click()
  }

  return (
    <div className="h-[calc(100vh-16rem)] flex flex-col">
      {/* Welcome Message */}
      {messages.length === 0 && (
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <div className="max-w-3xl text-center">
            <h2 className="text-3xl font-bold gradient-text mb-4">
              Ask me anything about India's agricultural and climate data
            </h2>
            <p className="text-gray-600 mb-8">
              I can help you analyze crop production, rainfall patterns, and their correlations across states and districts.
              All answers are backed by official data from data.gov.in with complete source citations.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              {SAMPLE_QUESTIONS.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSampleQuestion(question)}
                  className="card p-4 text-left hover:bg-green-50 transition-colors group"
                >
                  <BookOpen className="w-5 h-5 text-green-600 mb-2 group-hover:scale-110 transition-transform" />
                  <p className="text-sm text-gray-700">{question}</p>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      {messages.length > 0 && (
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl ${
                  message.role === 'user'
                    ? 'bg-green-600 text-white rounded-lg p-4'
                    : 'card p-6 w-full'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      <span className="text-sm font-semibold text-gray-700">
                        Project Samarth
                      </span>
                      {message.confidence && (
                        <span className="text-xs text-gray-500">
                          {(message.confidence * 100).toFixed(0)}% confidence
                        </span>
                      )}
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => copyToClipboard(message.content, index)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                        title="Copy answer"
                      >
                        {copiedIndex === index ? (
                          <CheckCircle2 className="w-4 h-4 text-green-600" />
                        ) : (
                          <Copy className="w-4 h-4" />
                        )}
                      </button>
                    </div>
                  </div>
                )}
                
                <div className={message.role === 'user' ? '' : 'prose prose-sm max-w-none'}>
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                {message.dataSources && message.dataSources.length > 0 && (
                  <div className="mt-6 pt-4 border-t border-gray-200">
                    <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                      <Database className="w-4 h-4 mr-2" />
                      Data Sources Used
                    </h4>
                    <div className="space-y-2">
                      {message.dataSources.map((source, idx) => (
                        <div key={idx} className="text-xs bg-gray-50 p-3 rounded-lg">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <p className="font-semibold text-gray-800">
                                {source.dataset_name}
                              </p>
                              <p className="text-gray-600 mt-1">
                                {source.description}
                              </p>
                            </div>
                            <a
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="ml-2 text-green-600 hover:text-green-700 font-medium"
                            >
                              View →
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {message.processingTime && (
                  <div className="mt-4 text-xs text-gray-500">
                    Processed in {message.processingTime.toFixed(2)}s
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="card p-6 max-w-3xl">
                <div className="flex items-center space-x-3">
                  <Loader2 className="w-5 h-5 text-green-600 animate-spin" />
                  <span className="text-gray-600">
                    Analyzing data sources and generating answer...
                  </span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <div className="max-w-4xl mx-auto">
          {messages.length > 0 && (
            <div className="mb-3 flex justify-end">
              <button
                onClick={exportConversation}
                className="text-sm text-gray-600 hover:text-green-600 flex items-center space-x-2"
              >
                <Download className="w-4 h-4" />
                <span>Export Conversation</span>
              </button>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about agricultural or climate data..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="btn-primary flex items-center space-x-2"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              <span>Send</span>
            </button>
          </form>
          
          <p className="text-xs text-gray-500 mt-2 text-center">
            All data is sourced from official government portals and cited in responses
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
