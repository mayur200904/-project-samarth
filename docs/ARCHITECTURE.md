# 🏗️ System Architecture

## Overview

Project Samarth is built on a modern, scalable architecture designed to handle complex data queries across multiple government datasets while maintaining high performance and complete traceability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                       (React Frontend)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Chat         │  │ Data         │  │ About /      │          │
│  │ Interface    │  │ Explorer     │  │ Documentation│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             │ JSON
┌────────────────────────────▼────────────────────────────────────┐
│                        API GATEWAY                               │
│                      (FastAPI Backend)                           │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              API Routes & Middleware                 │       │
│  │  /chat │ /datasets │ /health │ CORS │ Error Handler │       │
│  └────────────────────────┬─────────────────────────────┘       │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ Query Engine   │  │ LLM Service    │  │ RAG Service      │  │
│  │                │  │                │  │                  │  │
│  │ - Orchestrates │  │ - Query        │  │ - Vector DB      │  │
│  │   pipeline     │  │   decomposition│  │ - Semantic       │  │
│  │ - Processes    │  │ - Answer       │  │   search         │  │
│  │   queries      │  │   generation   │  │ - Dataset        │  │
│  │ - Synthesizes  │  │ - Entity       │  │   indexing       │  │
│  │   results      │  │   extraction   │  │ - Relevance      │  │
│  │                │  │                │  │   scoring        │  │
│  └────────┬───────┘  └────────┬───────┘  └─────────┬────────┘  │
└───────────┼──────────────────┼─────────────────────┼───────────┘
            │                  │                     │
            │                  │                     │
┌───────────▼──────────────────▼─────────────────────▼───────────┐
│                      DATA ACCESS LAYER                           │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ Data Fetcher   │  │ ChromaDB       │  │ Cache Manager    │  │
│  │                │  │                │  │                  │  │
│  │ - data.gov.in  │  │ - Vector store │  │ - Redis (opt)    │  │
│  │   API client   │  │ - Embeddings   │  │ - Parquet files  │  │
│  │ - CSV/JSON/XLS │  │ - Collections  │  │ - TTL management │  │
│  │   parsers      │  │ - Similarity   │  │                  │  │
│  │ - Normalizer   │  │   search       │  │                  │  │
│  └────────┬───────┘  └────────────────┘  └──────────────────┘  │
└───────────┼─────────────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                         │
│  ┌────────────────────────┐  ┌──────────────────────────────┐  │
│  │ data.gov.in API        │  │ Local Cache Storage          │  │
│  │ - Agriculture datasets │  │ - ./data/*.parquet           │  │
│  │ - Climate datasets     │  │ - ./chroma_db/               │  │
│  │ - Real-time updates    │  │                              │  │
│  └────────────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ LLM Providers (Choose one)                                 │ │
│  │  - OpenAI GPT-4     │ - Anthropic Claude                   │ │
│  │  - Google Gemini    │ - Ollama (Local)                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (React)

**Technology Stack:**
- React 18 with Hooks
- Vite for build tooling
- TailwindCSS for styling
- React Query for data fetching
- Axios for HTTP client

**Key Components:**
- **ChatInterface**: Main conversational UI with message history, citations display, and export functionality
- **DataExplorer**: Browse and search available datasets with filtering and refresh capabilities
- **About**: System documentation and feature showcase

**Responsibilities:**
- User interaction and experience
- API communication
- Real-time updates and loading states
- Citation visualization
- Conversation management

### 2. API Gateway (FastAPI)

**Technology Stack:**
- FastAPI for REST API
- Uvicorn as ASGI server
- Pydantic for data validation
- CORS middleware

**Endpoints:**
- `POST /api/v1/chat` - Process user queries
- `GET /api/v1/datasets` - List available datasets
- `GET /api/v1/datasets/{id}` - Get dataset details
- `POST /api/v1/datasets/query` - Query dataset with filters
- `POST /api/v1/datasets/{id}/refresh` - Refresh dataset from source
- `GET /api/v1/health` - Health check

**Features:**
- Automatic API documentation (Swagger/ReDoc)
- Request/response validation
- Error handling and logging
- CORS configuration
- Rate limiting (future)

### 3. Business Logic Layer

#### 3.1 Query Engine

**File**: `backend/app/services/query_engine.py`

**Pipeline:**
1. **Query Decomposition**: Break complex questions into sub-queries
2. **Dataset Selection**: Identify relevant datasets using RAG
3. **Data Retrieval**: Fetch and filter data from selected datasets
4. **Answer Generation**: Synthesize comprehensive answer with LLM
5. **Citation Extraction**: Map claims to source datasets

**Key Methods:**
- `process_query()` - Main orchestration method
- `_retrieve_data()` - Multi-source data fetching
- `_build_filters()` - Convert entities to dataset filters
- `_summarize_dataframe()` - Aggregate large datasets

#### 3.2 LLM Service

**File**: `backend/app/services/llm_service.py`

**Supported Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Ollama (Local models)

**Capabilities:**
- Query decomposition with structured output
- Entity extraction (states, crops, years, etc.)
- Answer generation with context
- Citation identification
- Multi-turn conversations

**Design Patterns:**
- Strategy pattern for provider selection
- Async/await for non-blocking I/O
- Retry logic with exponential backoff
- Token optimization

#### 3.3 RAG Service

**File**: `backend/app/services/rag_service.py`

**Technology:**
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- Cosine similarity for matching

**Indexing Strategy:**
1. **Dataset-level documents**: Name, description, metadata
2. **Column-level documents**: Individual field information
3. **Sample data**: Representative data points

**Search Process:**
1. Embed user query
2. Find top-k similar documents
3. Extract unique datasets
4. Return with relevance scores

### 4. Data Access Layer

#### 4.1 Data Fetcher

**File**: `backend/app/services/data_fetcher.py`

**Data Sources:**
```python
DATASETS = {
    "crop_production": {...},
    "rainfall_data": {...},
    "area_production": {...},
    "climate_data": {...},
    "agri_prices": {...}
}
```

**Features:**
- Async HTTP client for API calls
- Multi-format parsing (CSV, JSON, XLS)
- Automatic caching with TTL
- Data normalization
- Sample data generation (for demo)

**Cache Strategy:**
- Parquet format for efficiency
- TTL-based invalidation
- Manual refresh capability
- Incremental updates

#### 4.2 Vector Database (ChromaDB)

**Configuration:**
- Persistent storage in `./chroma_db/`
- Default embedding function (all-MiniLM-L6-v2)
- Collection: "datasets"

**Metadata:**
```python
{
    "dataset_key": "crop_production",
    "name": "Crop Production Statistics",
    "category": "agriculture",
    "columns": ["State", "Crop", "Year", ...],
    "row_count": 12345
}
```

## Data Flow

### Query Processing Flow

```
User Question
    │
    ▼
┌──────────────────────────┐
│ 1. Query Decomposition   │
│    - Extract intent      │
│    - Identify entities   │
│    - Generate sub-queries│
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ 2. Semantic Search (RAG) │
│    - Embed query         │
│    - Find datasets       │
│    - Rank by relevance   │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ 3. Data Retrieval        │
│    - Fetch datasets      │
│    - Apply filters       │
│    - Aggregate/summarize │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ 4. Answer Generation     │
│    - Create context      │
│    - Call LLM            │
│    - Extract citations   │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ 5. Response Assembly     │
│    - Format answer       │
│    - Attach sources      │
│    - Calculate confidence│
└───────────┬──────────────┘
            │
            ▼
      JSON Response
```

### Data Ingestion Flow

```
data.gov.in API
    │
    ▼
┌──────────────────────────┐
│ HTTP GET Request         │
│ (with API key if needed) │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Format Detection &       │
│ Parsing                  │
│ (CSV/JSON/XLS)          │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Data Normalization       │
│ - Standardize columns    │
│ - Type conversion        │
│ - Handle missing values  │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Cache Storage            │
│ - Save as Parquet        │
│ - Update metadata        │
│ - Set TTL                │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Vector Indexing          │
│ - Create embeddings      │
│ - Store in ChromaDB      │
│ - Update collection      │
└──────────────────────────┘
```

## Scalability Considerations

### Current Architecture (Single Server)
- **Concurrent Users**: 100+
- **Response Time**: < 5 seconds
- **Data Volume**: 50+ datasets, millions of rows

### Horizontal Scaling Path

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│                     (nginx/HAProxy)                      │
└──────────────┬────────────────┬─────────────────────────┘
               │                │
       ┌───────▼──────┐  ┌──────▼────────┐
       │  Frontend 1  │  │  Frontend 2   │
       │  (Static)    │  │  (Static)     │
       └──────────────┘  └───────────────┘
                             │
                ┌────────────┴────────────┐
         ┌──────▼───────┐         ┌───────▼──────┐
         │  API Node 1  │         │  API Node 2  │
         │  (FastAPI)   │         │  (FastAPI)   │
         └──────┬───────┘         └───────┬──────┘
                │                         │
                └──────────┬──────────────┘
                           │
              ┌────────────▼──────────────┐
              │   Shared Services         │
              │  - Redis (Cache)          │
              │  - PostgreSQL (Metadata)  │
              │  - ChromaDB (Vectors)     │
              │  - S3 (Data Storage)      │
              └───────────────────────────┘
```

### Microservices Decomposition (Future)

- **Query Service**: Handle user queries
- **Data Service**: Manage datasets and caching
- **LLM Service**: Abstract LLM interactions
- **RAG Service**: Vector search and indexing
- **Citation Service**: Source tracking

## Security Architecture

### Authentication & Authorization (Future)
- JWT-based authentication
- Role-based access control (RBAC)
- API key management

### Data Security
- Encryption at rest (dataset cache)
- TLS/HTTPS in transit
- API key rotation
- Audit logging

### Privacy Considerations
- Local deployment option (Ollama)
- No external data leakage
- Configurable data retention
- GDPR compliance ready

## Performance Optimizations

### Current Optimizations
1. **Async I/O**: All I/O operations are non-blocking
2. **Caching**: Parquet files with TTL
3. **Connection Pooling**: Reuse HTTP connections
4. **Lazy Loading**: Load datasets on demand
5. **Response Streaming**: Stream large responses
6. **Vector Indexing**: Pre-computed embeddings

### Future Optimizations
1. **Query Result Caching**: Cache frequent queries
2. **Database Indexes**: Index common query patterns
3. **CDN**: Serve static frontend assets
4. **Compression**: Gzip API responses
5. **Batch Processing**: Process multiple queries
6. **Model Quantization**: Smaller embedding models

## Monitoring & Observability

### Metrics to Track
- Query response time (p50, p95, p99)
- API endpoint latency
- LLM API call duration
- Dataset fetch time
- Vector search latency
- Error rates
- Cache hit ratio

### Logging Strategy
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error stack traces
- Performance profiling

### Health Checks
- `/api/v1/health` endpoint
- Service dependency checks
- Database connectivity
- LLM provider status

## Technology Choices & Rationale

| Component | Technology | Why? |
|-----------|-----------|------|
| **Backend** | FastAPI | Modern, fast, async support, automatic docs |
| **Frontend** | React | Component-based, large ecosystem, performant |
| **Vector DB** | ChromaDB | Simple, embedded, good for prototypes |
| **LLM** | Multi-provider | Flexibility, avoid vendor lock-in |
| **Cache** | Parquet | Columnar, compressed, fast reads |
| **Build** | Vite | Fast, modern, good DX |
| **Styling** | TailwindCSS | Utility-first, rapid development |

## Future Enhancements

### Short-term (v2.0)
- [ ] Conversation history persistence
- [ ] User authentication
- [ ] Advanced visualizations (charts, maps)
- [ ] Export to PDF/Excel
- [ ] Multi-language support

### Long-term (v3.0+)
- [ ] Real-time collaborative queries
- [ ] Automated insights generation
- [ ] Predictive analytics
- [ ] Integration with more data sources
- [ ] Mobile app
- [ ] Voice interface
