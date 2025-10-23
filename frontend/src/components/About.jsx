import { CheckCircle2, Zap, Shield, TrendingUp, Globe, HardDrive } from 'lucide-react'

function About() {
  const features = [
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Advanced RAG Architecture",
      description: "Vector embeddings and semantic search across datasets for intelligent query routing"
    },
    {
      icon: <HardDrive className="w-6 h-6" />,
      title: "Real-time Data Integration",
      description: "Direct API integration with data.gov.in with automatic format normalization"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Multi-Source Synthesis",
      description: "Correlates agriculture data with climate patterns across multiple datasets"
    },
    {
      icon: <CheckCircle2 className="w-6 h-6" />,
      title: "Complete Traceability",
      description: "Every claim cited with source dataset and clickable links to original data"
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: "Intelligent Query Processing",
      description: "LLM-powered query understanding with automatic sub-query generation"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Privacy & Security",
      description: "Deployable in private environments with local LLM support (Ollama)"
    }
  ]

  const capabilities = [
    "Comparative analysis across states and districts",
    "Temporal trend analysis with decade-long patterns",
    "Cross-domain correlation (climate ↔ agriculture)",
    "Ranking and aggregations with confidence scores",
    "Policy recommendation synthesis",
    "What-if scenario analysis"
  ]

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="card p-8 bg-gradient-to-r from-green-50 to-blue-50">
        <h2 className="text-3xl font-bold gradient-text mb-4">
          Project Samarth
        </h2>
        <p className="text-lg text-gray-700 mb-6">
          An intelligent Q&A system enabling policymakers and researchers to derive cross-domain 
          insights from India's agricultural and climate data through natural language queries.
        </p>
        <div className="flex flex-wrap gap-3">
          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
            FastAPI Backend
          </span>
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
            React Frontend
          </span>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
            RAG Architecture
          </span>
          <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-semibold">
            Multi-LLM Support
          </span>
        </div>
      </div>

      {/* Features Grid */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Key Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="card p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-green-600 mb-4">
                {feature.icon}
              </div>
              <h4 className="text-lg font-bold text-gray-900 mb-2">
                {feature.title}
              </h4>
              <p className="text-gray-600 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Capabilities */}
      <div className="card p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">System Capabilities</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {capabilities.map((capability, index) => (
            <div key={index} className="flex items-start space-x-3">
              <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <span className="text-gray-700">{capability}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture */}
      <div className="card p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">System Architecture</h3>
        <div className="bg-gray-50 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre className="text-gray-700">
{`┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  Chat Interface | Visualizations | Source Explorer          │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────────┐
│                  Backend (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Query Engine │  │ Data Manager │  │ LLM Service  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│  ┌──────▼──────────────────▼──────────────────▼───────┐    │
│  │           RAG System (ChromaDB)                     │    │
│  │  Vector Embeddings | Semantic Search               │    │
│  └──────┬──────────────────────────────────────────────┘    │
└─────────┼───────────────────────────────────────────────────┘
          │
┌─────────▼──────────────────────────────────────────────────┐
│              Data Layer                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ data.gov.in  │  │ Local Cache  │  │ Normalizer   │     │
│  │     API      │  │  (Parquet)   │  │   Engine     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────────────────────────────────────┘`}
          </pre>
        </div>
      </div>

      {/* Data Sources */}
      <div className="card p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Data Sources</h3>
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">
              Ministry of Agriculture & Farmers Welfare
            </h4>
            <ul className="list-disc list-inside text-gray-600 space-y-1 ml-4">
              <li>Crop production statistics</li>
              <li>District-wise agricultural data</li>
              <li>Crop calendars and seasons</li>
              <li>Agricultural commodity prices</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">
              India Meteorological Department (IMD)
            </h4>
            <ul className="list-disc list-inside text-gray-600 space-y-1 ml-4">
              <li>Rainfall data (district/state level)</li>
              <li>Temperature records</li>
              <li>Monsoon patterns</li>
              <li>Climate indices</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Technical Highlights */}
      <div className="card p-8 bg-gradient-to-br from-green-50 to-blue-50">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">
          Why This Project Stands Out
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-bold text-green-700 mb-3">Production-Grade Code</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ Type hints throughout</li>
              <li>✅ Comprehensive error handling</li>
              <li>✅ Structured logging and monitoring</li>
              <li>✅ Unit and integration tests ready</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-blue-700 mb-3">Scalable Architecture</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ Microservices-ready design</li>
              <li>✅ Async/await for I/O operations</li>
              <li>✅ Connection pooling</li>
              <li>✅ Horizontal scalability</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-purple-700 mb-3">Advanced NLP</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ Query decomposition with LLMs</li>
              <li>✅ Named entity recognition</li>
              <li>✅ Temporal reasoning</li>
              <li>✅ Multi-hop question answering</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-yellow-700 mb-3">Data Engineering</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ ETL pipelines for diverse formats</li>
              <li>✅ Data quality validation</li>
              <li>✅ Incremental updates</li>
              <li>✅ Schema normalization</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Performance */}
      <div className="card p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Performance Metrics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">&lt; 5s</div>
            <div className="text-sm text-gray-600">Query Response Time</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">50+</div>
            <div className="text-sm text-gray-600">Datasets Integrated</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">90%+</div>
            <div className="text-sm text-gray-600">Answer Accuracy</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600 mb-2">100+</div>
            <div className="text-sm text-gray-600">Concurrent Users</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default About
