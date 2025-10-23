"""
RAG Service - Retrieval Augmented Generation
Implements vector database and semantic search for datasets
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
import logging
from typing import List, Dict, Any, Optional
import hashlib
import json

from app.core.config import settings
from app.services.data_fetcher import DataFetcher

logger = logging.getLogger(__name__)


class RAGService:
    """RAG service for semantic search over datasets"""
    
    def __init__(self):
        self.client: Optional[chromadb.Client] = None
        self.collection: Optional[chromadb.Collection] = None
        self.data_fetcher = DataFetcher()
        
    async def initialize(self):
        """Initialize ChromaDB and create collections"""
        logger.info("Initializing RAG service...")
        
        # Initialize ChromaDB with OpenAI embeddings (lighter than sentence-transformers)
        try:
            from chromadb.utils import embedding_functions
            
            # Use OpenAI embeddings if API key is available
            if settings.OPENAI_API_KEY:
                openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=settings.OPENAI_API_KEY,
                    model_name=settings.EMBEDDING_MODEL
                )
                
                self.client = chromadb.Client(ChromaSettings(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    anonymized_telemetry=False
                ))
                
                # Get or create collection with OpenAI embeddings
                self.collection = self.client.get_or_create_collection(
                    name="datasets",
                    embedding_function=openai_ef,
                    metadata={"description": "Agricultural and climate datasets metadata"}
                )
            else:
                # Fallback to default embeddings
                self.client = chromadb.Client(ChromaSettings(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    anonymized_telemetry=False
                ))
                
                self.collection = self.client.get_or_create_collection(
                    name="datasets",
                    metadata={"description": "Agricultural and climate datasets metadata"}
                )
        except Exception as e:
            logger.warning(f"Failed to initialize with OpenAI embeddings: {e}, using defaults")
            self.client = chromadb.Client(ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                anonymized_telemetry=False
            ))
            
            self.collection = self.client.get_or_create_collection(
                name="datasets",
                metadata={"description": "Agricultural and climate datasets metadata"}
            )
        
        # Index datasets if collection is empty
        if self.collection.count() == 0:
            await self._index_datasets()
        
        logger.info(f"RAG service initialized with {self.collection.count()} indexed documents")
    
    async def _index_datasets(self):
        """Index all datasets metadata for semantic search"""
        logger.info("Indexing datasets...")
        
        documents = []
        metadatas = []
        ids = []
        
        for key, dataset_info in self.data_fetcher.DATASETS.items():
            # Try to get actual data for better indexing
            try:
                df = await self.data_fetcher.fetch_dataset(key)
                
                # Create rich metadata document
                doc_text = f"""
                Dataset: {dataset_info['name']}
                Category: {dataset_info['category']}
                Description: {dataset_info['description']}
                Columns: {', '.join(df.columns.tolist())}
                Row Count: {len(df)}
                Sample Data: {df.head(3).to_string()}
                """
                
                metadata = {
                    "dataset_key": key,
                    "name": dataset_info['name'],
                    "category": dataset_info['category'],
                    "description": dataset_info['description'],
                    "url": dataset_info['url'],
                    "columns": json.dumps(df.columns.tolist()),
                    "row_count": len(df)
                }
                
                # Add column-specific documents for better matching
                for column in df.columns:
                    col_doc = f"""
                    Dataset: {dataset_info['name']}
                    Column: {column}
                    Sample Values: {df[column].dropna().unique()[:10].tolist()}
                    Data Type: {df[column].dtype}
                    """
                    
                    documents.append(col_doc)
                    metadatas.append({
                        **metadata,
                        "document_type": "column",
                        "column_name": column
                    })
                    ids.append(f"{key}_{column}")
                
                # Add dataset-level document
                documents.append(doc_text)
                metadatas.append({**metadata, "document_type": "dataset"})
                ids.append(key)
                
            except Exception as e:
                logger.error(f"Failed to index {key}: {e}")
        
        # Add to collection
        if documents:
            # ChromaDB will automatically generate embeddings
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Indexed {len(documents)} documents")
    
    def find_relevant_datasets(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find datasets relevant to a query using semantic search
        
        Args:
            query: User's question
            n_results: Number of results to return
            
        Returns:
            List of relevant datasets with metadata
        """
        if not self.collection:
            raise RuntimeError("RAG service not initialized")
        
        # Search the collection
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Extract unique datasets
        datasets = []
        seen_keys = set()
        
        if results['metadatas']:
            for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
                dataset_key = metadata.get('dataset_key')
                if dataset_key and dataset_key not in seen_keys:
                    datasets.append({
                        "dataset_key": dataset_key,
                        "name": metadata.get('name'),
                        "category": metadata.get('category'),
                        "description": metadata.get('description'),
                        "url": metadata.get('url'),
                        "relevance_score": 1 - distance  # Convert distance to similarity
                    })
                    seen_keys.add(dataset_key)
        
        return datasets
    
    def get_dataset_context(
        self,
        dataset_key: str,
        query: str
    ) -> str:
        """
        Get relevant context from a specific dataset for a query
        
        Args:
            dataset_key: The dataset to search in
            query: The query to find context for
            
        Returns:
            Context string with relevant information
        """
        # Query for documents from this dataset
        results = self.collection.query(
            query_texts=[query],
            n_results=10,
            where={"dataset_key": dataset_key}
        )
        
        if not results['documents'] or not results['documents'][0]:
            return ""
        
        # Combine relevant documents
        context_parts = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            if metadata.get('document_type') == 'column':
                context_parts.append(f"Column {metadata.get('column_name')}: {doc}")
            else:
                context_parts.append(doc)
        
        return "\n\n".join(context_parts[:5])  # Limit to top 5 most relevant
    
    async def close(self):
        """Cleanup resources"""
        await self.data_fetcher.close()
