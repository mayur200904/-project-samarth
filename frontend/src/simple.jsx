import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

function SimpleApp() {
  const [message, setMessage] = React.useState('')
  const [response, setResponse] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  const askQuestion = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      })
      const data = await res.json()
      setResponse(data)
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#059669' }}>🌾 Project Samarth - Simple Test</h1>
      
      <div style={{ marginTop: '20px' }}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a question..."
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            border: '2px solid #059669',
            borderRadius: '4px'
          }}
        />
        <button
          onClick={askQuestion}
          disabled={loading || !message}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            fontSize: '16px',
            background: '#059669',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'wait' : 'pointer'
          }}
        >
          {loading ? 'Processing...' : 'Ask Question'}
        </button>
      </div>

      {response && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#f0fdf4', borderRadius: '4px' }}>
          <h3>Answer:</h3>
          <p>{response.answer.substring(0, 500)}...</p>
          <p><strong>Citations:</strong> {response.citations.length}</p>
          <p><strong>Processing Time:</strong> {response.processing_time.toFixed(2)}s</p>
        </div>
      )}
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<SimpleApp />)
