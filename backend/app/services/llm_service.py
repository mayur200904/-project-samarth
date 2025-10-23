"""
LLM Service - Language Model Integration
Handles query decomposition, answer generation, and multi-LLM support
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
import json
import asyncio
from enum import Enum

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"


class LLMService:
    """Service for LLM interactions"""
    
    def __init__(self):
        self.provider = LLMProvider(settings.LLM_PROVIDER)
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        try:
            if self.provider == LLMProvider.OPENAI:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                self.model = settings.MODEL_NAME
                logger.info(f"Initialized OpenAI client with model {self.model}")
                
            elif self.provider == LLMProvider.ANTHROPIC:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
                self.model = "claude-3-sonnet-20240229"
                logger.info(f"Initialized Anthropic client with model {self.model}")
                
            elif self.provider == LLMProvider.GOOGLE:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = "gemini-pro"
                logger.info(f"Initialized Google client with model {self.model}")
                
            elif self.provider == LLMProvider.OLLAMA:
                # Ollama uses a local endpoint
                import aiohttp
                self.client = aiohttp.ClientSession()
                self.model = settings.OLLAMA_MODEL
                self.ollama_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
                logger.info(f"Initialized Ollama client with model {self.model}")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise
    
    async def decompose_query(self, user_query: str) -> Dict[str, Any]:
        """
        Decompose a complex query into sub-queries and identify required data
        
        Returns:
            {
                "intent": "comparison|trend|correlation|ranking|recommendation",
                "sub_queries": ["sub-query 1", "sub-query 2", ...],
                "required_data": {
                    "states": [...],
                    "crops": [...],
                    "time_period": {...},
                    "metrics": [...]
                },
                "query_type": "agricultural|climate|mixed"
            }
        """
        prompt = f"""You are an expert at analyzing questions about agricultural and climate data.

Analyze this question and extract:
1. The user's intent (comparison, trend_analysis, correlation, ranking, recommendation, or general)
2. Break it into specific sub-queries that can be answered with data
3. Identify required data elements (states, districts, crops, time periods, metrics)
4. Classify the query type (agricultural, climate, or mixed)

Question: {user_query}

Respond in JSON format:
{{
    "intent": "comparison|trend_analysis|correlation|ranking|recommendation|general",
    "sub_queries": ["specific data query 1", "specific data query 2"],
    "required_data": {{
        "states": ["state1", "state2"],
        "districts": ["district1"],
        "crops": ["crop1", "crop2"],
        "time_period": {{"start_year": 2013, "end_year": 2023}},
        "metrics": ["production", "rainfall", "area"]
    }},
    "query_type": "agricultural|climate|mixed"
}}"""

        response = await self._call_llm(prompt)
        
        try:
            # Extract JSON from response
            result = self._extract_json(response)
            return result
        except Exception as e:
            logger.error(f"Failed to parse query decomposition: {e}")
            # Return a default structure
            return {
                "intent": "general",
                "sub_queries": [user_query],
                "required_data": {},
                "query_type": "mixed"
            }
    
    async def generate_answer(
        self,
        user_query: str,
        data_context: Dict[str, Any],
        dataset_info: List[Dict[str, Any]]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Generate an answer based on retrieved data
        
        Args:
            user_query: Original user question
            data_context: Retrieved data from datasets
            dataset_info: Information about datasets used
            
        Returns:
            (answer_text, citations)
        """
        # Format data context
        context_str = self._format_data_context(data_context)
        datasets_str = self._format_datasets(dataset_info)
        
        prompt = f"""You are an expert agricultural policy analyst with deep knowledge of Indian agriculture and climate patterns.

User Question: {user_query}

Available Data:
{context_str}

Data Sources:
{datasets_str}

Instructions:
1. Provide a comprehensive, accurate answer based ONLY on the provided data
2. Be specific with numbers, percentages, and trends
3. For each claim you make, indicate which data source(s) it comes from using [Source: dataset_name]
4. If the data is insufficient to answer fully, clearly state what's missing
5. Structure your answer clearly with relevant headings
6. Use tables or bullet points where appropriate
7. Provide actionable insights when relevant

Answer:"""

        answer = await self._call_llm(prompt)
        
        # Extract citations
        citations = self._extract_citations(answer, dataset_info)
        
        return answer, citations
    
    async def extract_entities(self, query: str) -> Dict[str, List[str]]:
        """
        Extract named entities from query (states, crops, etc.)
        
        Returns:
            {
                "states": [...],
                "districts": [...],
                "crops": [...],
                "years": [...]
            }
        """
        prompt = f"""Extract all mentions of Indian states, districts, crops, and years from this query.

Query: {query}

Known states include: Punjab, Haryana, Uttar Pradesh, Maharashtra, West Bengal, Karnataka, Tamil Nadu, Andhra Pradesh, Gujarat, Madhya Pradesh, etc.

Known crops include: Rice, Wheat, Maize, Cotton, Sugarcane, Soybean, Groundnut, Jowar, Bajra, Pulses, Millets, etc.

Respond in JSON format:
{{
    "states": ["state1", "state2"],
    "districts": ["district1"],
    "crops": ["crop1", "crop2"],
    "years": [2020, 2021]
}}

If none found for a category, use an empty list."""

        response = await self._call_llm(prompt)
        
        try:
            return self._extract_json(response)
        except:
            return {"states": [], "districts": [], "crops": [], "years": []}
    
    async def _call_llm(self, prompt: str, temperature: float = 0.3) -> str:
        """Call the configured LLM provider"""
        try:
            if self.provider == LLMProvider.OPENAI:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides accurate, data-driven answers."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                return response.choices[0].message.content
                
            elif self.provider == LLMProvider.ANTHROPIC:
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                return response.content[0].text
                
            elif self.provider == LLMProvider.GOOGLE:
                import google.generativeai as genai
                model = genai.GenerativeModel(self.model)
                response = await model.generate_content_async(prompt)
                return response.text
                
            elif self.provider == LLMProvider.OLLAMA:
                async with self.client.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature
                    }
                ) as response:
                    result = await response.json()
                    return result.get("response", "")
                    
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response"""
        # Try to find JSON in the response
        import re
        
        # Look for JSON block
        json_match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find raw JSON
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        
        # Try parsing the whole response
        return json.loads(text)
    
    def _format_data_context(self, data_context: Dict[str, Any]) -> str:
        """Format data context for LLM prompt"""
        parts = []
        for dataset_key, data in data_context.items():
            if isinstance(data, list) and data:
                parts.append(f"\n{dataset_key.upper()}:")
                parts.append(json.dumps(data[:50], indent=2))  # Limit to first 50 rows
            elif isinstance(data, str):
                parts.append(f"\n{dataset_key.upper()}:")
                parts.append(data)
        
        return "\n".join(parts)
    
    def _format_datasets(self, dataset_info: List[Dict[str, Any]]) -> str:
        """Format dataset information"""
        parts = []
        for ds in dataset_info:
            parts.append(f"- {ds.get('name', '')}: {ds.get('description', '')} ({ds.get('url', '')})")
        return "\n".join(parts)
    
    def _extract_citations(
        self,
        answer: str,
        dataset_info: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract citations from the answer"""
        import re
        
        citations = []
        
        # Find all [Source: ...] patterns
        source_pattern = r'\[Source:\s*([^\]]+)\]'
        matches = re.finditer(source_pattern, answer)
        
        for match in matches:
            source_name = match.group(1).strip()
            # Find matching dataset
            for ds in dataset_info:
                if source_name.lower() in ds.get('name', '').lower():
                    citations.append({
                        "claim": "Referenced in answer",
                        "source": ds,
                        "confidence": 0.9
                    })
                    break
        
        # If no explicit citations found, cite all used datasets
        if not citations:
            for ds in dataset_info:
                citations.append({
                    "claim": "Data source used",
                    "source": ds,
                    "confidence": 0.8
                })
        
        return citations
    
    async def close(self):
        """Cleanup resources"""
        if self.provider == LLMProvider.OLLAMA and self.client:
            await self.client.close()
