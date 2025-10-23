"""
Query Engine - Orchestrates the entire query processing pipeline
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import uuid

from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.data_fetcher import DataFetcher
from app.models.schemas import ChatResponse, QueryType, Citation, DataSource

logger = logging.getLogger(__name__)


class QueryEngine:
    """Main query processing engine"""
    
    def __init__(
        self,
        llm_service: LLMService,
        rag_service: RAGService,
        data_fetcher: DataFetcher
    ):
        self.llm_service = llm_service
        self.rag_service = rag_service
        self.data_fetcher = data_fetcher
    
    async def process_query(
        self,
        user_query: str,
        conversation_id: Optional[str] = None
    ) -> ChatResponse:
        """
        Process a user query end-to-end
        
        Pipeline:
        1. Query decomposition (extract intent, entities, sub-queries)
        2. Dataset selection (find relevant datasets using RAG)
        3. Data retrieval (fetch and filter data)
        4. Answer generation (use LLM to synthesize answer)
        5. Citation extraction (identify sources for claims)
        """
        start_time = datetime.utcnow()
        
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        logger.info(f"Processing query [{conversation_id}]: {user_query}")
        
        try:
            # Step 1: Decompose query
            logger.info("Step 1: Decomposing query...")
            decomposition = await self.llm_service.decompose_query(user_query)
            logger.info(f"Query decomposition: {decomposition}")
            
            # Determine query type
            query_type = self._map_intent_to_query_type(decomposition.get("intent", "general"))
            sub_queries = decomposition.get("sub_queries", [user_query])
            
            # Step 2: Find relevant datasets
            logger.info("Step 2: Finding relevant datasets...")
            relevant_datasets = self.rag_service.find_relevant_datasets(
                query=user_query,
                n_results=5
            )
            logger.info(f"Found {len(relevant_datasets)} relevant datasets")
            
            # Step 3: Retrieve data
            logger.info("Step 3: Retrieving data...")
            data_context = await self._retrieve_data(
                decomposition=decomposition,
                datasets=relevant_datasets
            )
            
            # Step 4: Generate answer
            logger.info("Step 4: Generating answer...")
            answer_text, citations = await self.llm_service.generate_answer(
                user_query=user_query,
                data_context=data_context,
                dataset_info=relevant_datasets
            )
            
            # Step 5: Create data sources list
            data_sources = [
                DataSource(
                    dataset_id=ds.get("dataset_key", ""),
                    dataset_name=ds.get("name", ""),
                    organization=ds.get("category", ""),
                    url=ds.get("url", ""),
                    description=ds.get("description", "")
                )
                for ds in relevant_datasets
            ]
            
            # Convert citations to proper format
            citation_objects = [
                Citation(
                    claim=cit.get("claim", ""),
                    sources=[
                        DataSource(
                            dataset_id=cit.get("source", {}).get("dataset_key", ""),
                            dataset_name=cit.get("source", {}).get("name", ""),
                            organization=cit.get("source", {}).get("category", ""),
                            url=cit.get("source", {}).get("url", ""),
                            description=cit.get("source", {}).get("description", "")
                        )
                    ],
                    confidence=cit.get("confidence", 0.8)
                )
                for cit in citations
            ]
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create response
            response = ChatResponse(
                answer=answer_text,
                citations=citation_objects,
                query_type=query_type,
                sub_queries=sub_queries,
                data_sources_used=data_sources,
                confidence=self._calculate_confidence(data_context, citations),
                processing_time=processing_time,
                conversation_id=conversation_id
            )
            
            logger.info(f"Query processed successfully in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}", exc_info=True)
            raise
    
    async def _retrieve_data(
        self,
        decomposition: Dict[str, Any],
        datasets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Retrieve relevant data from selected datasets
        """
        data_context = {}
        required_data = decomposition.get("required_data", {})
        
        # Determine which datasets to query based on query type
        query_type = decomposition.get("query_type", "mixed")
        
        for dataset in datasets[:3]:  # Limit to top 3 most relevant
            dataset_key = dataset.get("dataset_key")
            if not dataset_key:
                continue
            
            try:
                # Build filters based on required data
                filters = self._build_filters(required_data, dataset_key)
                
                # Fetch data
                df = await self.data_fetcher.query_dataset(
                    dataset_key=dataset_key,
                    filters=filters,
                    limit=1000
                )
                
                # Process and summarize data
                if not df.empty:
                    # For large datasets, provide summary statistics
                    if len(df) > 100:
                        summary = self._summarize_dataframe(df, required_data)
                        data_context[dataset_key] = summary
                    else:
                        # For smaller datasets, provide full data
                        data_context[dataset_key] = df.to_dict(orient="records")
                
            except Exception as e:
                logger.warning(f"Failed to retrieve data from {dataset_key}: {e}")
        
        return data_context
    
    def _build_filters(
        self,
        required_data: Dict[str, Any],
        dataset_key: str
    ) -> Dict[str, Any]:
        """Build filters for dataset query"""
        filters = {}
        
        # State filter
        if "states" in required_data and required_data["states"]:
            filters["State"] = required_data["states"]
        
        # Crop filter (only for agricultural datasets)
        if "crops" in required_data and required_data["crops"]:
            if dataset_key in ["crop_production", "area_production"]:
                filters["Crop"] = required_data["crops"]
        
        # Year filter
        if "time_period" in required_data:
            period = required_data["time_period"]
            if "start_year" in period and "end_year" in period:
                # Note: This is a simple filter. For range filtering, we'd need to modify query_dataset
                years = list(range(period["start_year"], period["end_year"] + 1))
                filters["Year"] = years
        
        return filters
    
    def _summarize_dataframe(
        self,
        df: pd.DataFrame,
        required_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Summarize a large dataframe into key statistics
        """
        summary = []
        
        # Group by relevant columns and aggregate
        groupby_cols = []
        if "State" in df.columns:
            groupby_cols.append("State")
        if "Crop" in df.columns and "crops" in required_data:
            groupby_cols.append("Crop")
        if "Year" in df.columns:
            groupby_cols.append("Year")
        
        if groupby_cols:
            # Find numeric columns to aggregate
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols and groupby_cols:
                grouped = df.groupby(groupby_cols)[numeric_cols].agg(['mean', 'sum', 'count'])
                summary_df = grouped.reset_index()
                
                # Flatten multi-level columns
                summary_df.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col 
                                      for col in summary_df.columns]
                
                summary = summary_df.to_dict(orient="records")[:100]  # Limit to 100 summary rows
        
        # If no grouping possible, return sample
        if not summary:
            summary = df.sample(min(50, len(df))).to_dict(orient="records")
        
        return summary
    
    def _map_intent_to_query_type(self, intent: str) -> QueryType:
        """Map LLM intent to QueryType enum"""
        mapping = {
            "comparison": QueryType.COMPARISON,
            "trend_analysis": QueryType.TREND_ANALYSIS,
            "correlation": QueryType.CORRELATION,
            "ranking": QueryType.RANKING,
            "recommendation": QueryType.RECOMMENDATION,
            "general": QueryType.GENERAL
        }
        return mapping.get(intent, QueryType.GENERAL)
    
    def _calculate_confidence(
        self,
        data_context: Dict[str, Any],
        citations: List[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score for the answer"""
        # Base confidence
        confidence = 0.5
        
        # Increase confidence if we have data
        if data_context:
            confidence += 0.2
        
        # Increase confidence based on number of data sources
        num_sources = len(data_context)
        confidence += min(0.2, num_sources * 0.05)
        
        # Increase confidence if we have citations
        if citations:
            confidence += 0.1
        
        return min(1.0, confidence)
