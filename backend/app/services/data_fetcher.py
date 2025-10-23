"""
Data Fetcher Service
Integrates with data.gov.in API to fetch agricultural and climate datasets
"""
import aiohttp
import asyncio
import pandas as pd
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

from app.core.config import settings

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetches and manages data from data.gov.in"""
    
    # Key datasets from data.gov.in
    DATASETS = {
        # Agricultural datasets
        "crop_production": {
            "id": "9ef84268-d588-465a-a308-a864a43d0070",
            "name": "Crop Production Statistics",
            "url": "https://data.gov.in/resource/crop-production-statistics",
            "category": "agriculture",
            "description": "District-wise crop production data across India"
        },
        "area_production": {
            "id": "d9d2d2d8-8f8a-4f8a-8f8a-8f8a8f8a8f8a",
            "name": "Area and Production of Crops",
            "url": "https://data.gov.in/resource/area-production-crops",
            "category": "agriculture",
            "description": "State-wise area and production statistics for various crops"
        },
        "rainfall_data": {
            "id": "rainfall-subdivision-1901-2017",
            "name": "Rainfall Data (IMD)",
            "url": "https://data.gov.in/resource/rainfall-data-imd",
            "category": "climate",
            "description": "Monthly rainfall data from India Meteorological Department"
        },
        "climate_data": {
            "id": "climate-temperature-data",
            "name": "Temperature Data (IMD)",
            "url": "https://data.gov.in/resource/climate-data-imd",
            "category": "climate",
            "description": "Temperature and climate indicators"
        },
        "agri_prices": {
            "id": "agricultural-prices",
            "name": "Agricultural Commodity Prices",
            "url": "https://data.gov.in/resource/agricultural-prices",
            "category": "agriculture",
            "description": "Market prices for agricultural commodities"
        }
    }
    
    def __init__(self):
        self.cache_dir = Path(settings.DATA_DIRECTORY)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict[str, Any] = {}
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _get_cache_path(self, dataset_id: str) -> Path:
        """Get cache file path for dataset"""
        return self.cache_dir / f"{dataset_id}.parquet"
    
    def _is_cache_valid(self, dataset_id: str) -> bool:
        """Check if cached data is still valid"""
        cache_path = self._get_cache_path(dataset_id)
        if not cache_path.exists():
            return False
        
        # Check cache age
        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(seconds=settings.CACHE_TTL)
    
    async def fetch_dataset(
        self, 
        dataset_key: str, 
        force_refresh: bool = False
    ) -> pd.DataFrame:
        """
        Fetch a dataset from data.gov.in or cache
        
        Args:
            dataset_key: Key from DATASETS dict
            force_refresh: Force refresh from API even if cache is valid
            
        Returns:
            DataFrame with the dataset
        """
        if dataset_key not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset_key}")
        
        dataset_info = self.DATASETS[dataset_key]
        cache_path = self._get_cache_path(dataset_key)
        
        # Check cache first
        if not force_refresh and self._is_cache_valid(dataset_key):
            logger.info(f"Loading {dataset_key} from cache")
            return pd.read_parquet(cache_path)
        
        # Fetch from API or fallback to sample data
        logger.info(f"Fetching {dataset_key} from data.gov.in")
        
        try:
            df = await self._fetch_from_api(dataset_info)
        except Exception as e:
            logger.warning(f"API fetch failed: {e}. Using sample data.")
            df = await self._generate_sample_data(dataset_key)
        
        # Cache the data
        df.to_parquet(cache_path, index=False)
        logger.info(f"Cached {dataset_key} with {len(df)} rows")
        
        return df
    
    async def _fetch_from_api(self, dataset_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Fetch data from data.gov.in API
        
        Note: data.gov.in API access requires registration and API key.
        This implementation includes fallback to sample data for demo purposes.
        """
        session = await self._get_session()
        
        # Construct API URL (this is a template - actual endpoints vary by dataset)
        api_url = f"{settings.DATA_GOV_BASE_URL}/{dataset_info['id']}"
        
        headers = {}
        if settings.DATA_GOV_API_KEY:
            headers["api-key"] = settings.DATA_GOV_API_KEY
        
        params = {
            "format": "json",
            "limit": 10000  # Adjust based on dataset size
        }
        
        async with session.get(api_url, headers=headers, params=params, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                # Handle different response formats
                if isinstance(data, dict) and "records" in data:
                    df = pd.DataFrame(data["records"])
                elif isinstance(data, list):
                    df = pd.DataFrame(data)
                else:
                    raise ValueError(f"Unexpected API response format: {type(data)}")
                
                return df
            else:
                raise Exception(f"API returned status {response.status}")
    
    async def _generate_sample_data(self, dataset_key: str) -> pd.DataFrame:
        """
        Generate realistic sample data for demo purposes
        This allows the system to work without API access
        """
        logger.info(f"Generating sample data for {dataset_key}")
        
        if dataset_key == "crop_production":
            return self._generate_crop_production_sample()
        elif dataset_key == "rainfall_data":
            return self._generate_rainfall_sample()
        elif dataset_key == "area_production":
            return self._generate_area_production_sample()
        elif dataset_key == "climate_data":
            return self._generate_climate_sample()
        elif dataset_key == "agri_prices":
            return self._generate_prices_sample()
        else:
            return pd.DataFrame()
    
    def _generate_crop_production_sample(self) -> pd.DataFrame:
        """Generate sample crop production data"""
        states = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "West Bengal", 
                  "Madhya Pradesh", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat"]
        crops = ["Rice", "Wheat", "Maize", "Jowar", "Bajra", "Cotton", "Sugarcane", 
                 "Groundnut", "Soybean", "Pulses"]
        years = range(2013, 2024)
        
        data = []
        for state in states:
            for crop in crops:
                for year in years:
                    # Generate realistic values based on crop and state
                    base_production = 1000 if crop in ["Rice", "Wheat"] else 500
                    variation = (hash(f"{state}{crop}{year}") % 500) - 250
                    
                    data.append({
                        "State": state,
                        "District": f"{state}_District_{hash(state+crop) % 5 + 1}",
                        "Crop": crop,
                        "Crop_Type": "Cereal" if crop in ["Rice", "Wheat", "Maize", "Jowar", "Bajra"] else "Cash Crop",
                        "Year": year,
                        "Season": "Kharif" if crop in ["Rice", "Maize", "Cotton"] else "Rabi",
                        "Area": abs(base_production * 2 + variation),
                        "Production": abs(base_production + variation),
                        "Yield": abs(2.5 + (variation / 200))
                    })
        
        return pd.DataFrame(data)
    
    def _generate_rainfall_sample(self) -> pd.DataFrame:
        """Generate sample rainfall data"""
        states = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "West Bengal",
                  "Madhya Pradesh", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Gujarat"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        years = range(2013, 2024)
        
        data = []
        for state in states:
            for year in years:
                for month_idx, month in enumerate(months):
                    # Monsoon months have higher rainfall
                    is_monsoon = month in ["Jun", "Jul", "Aug", "Sep"]
                    base_rainfall = 200 if is_monsoon else 30
                    variation = (hash(f"{state}{year}{month}") % 100) - 50
                    
                    data.append({
                        "State": state,
                        "Year": year,
                        "Month": month,
                        "Rainfall_mm": max(0, base_rainfall + variation),
                        "District": f"{state}_District_Central"
                    })
        
        return pd.DataFrame(data)
    
    def _generate_area_production_sample(self) -> pd.DataFrame:
        """Generate sample area and production data"""
        # Similar to crop production but aggregated at state level
        df = self._generate_crop_production_sample()
        return df.groupby(["State", "Crop", "Year", "Crop_Type"]).agg({
            "Area": "sum",
            "Production": "sum"
        }).reset_index()
    
    def _generate_climate_sample(self) -> pd.DataFrame:
        """Generate sample climate/temperature data"""
        states = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "West Bengal"]
        years = range(2013, 2024)
        months = range(1, 13)
        
        data = []
        for state in states:
            for year in years:
                for month in months:
                    # Temperature varies by season
                    base_temp = 25 + 10 * abs(month - 6.5) / 6.5
                    variation = (hash(f"{state}{year}{month}") % 10) - 5
                    
                    data.append({
                        "State": state,
                        "Year": year,
                        "Month": month,
                        "Max_Temperature": base_temp + 5 + variation,
                        "Min_Temperature": base_temp - 5 + variation,
                        "Avg_Temperature": base_temp + variation
                    })
        
        return pd.DataFrame(data)
    
    def _generate_prices_sample(self) -> pd.DataFrame:
        """Generate sample agricultural prices"""
        crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane"]
        states = ["Punjab", "Haryana", "Maharashtra", "Uttar Pradesh"]
        years = range(2013, 2024)
        
        data = []
        for crop in crops:
            base_price = 2000 if crop in ["Rice", "Wheat"] else 1500
            for state in states:
                for year in years:
                    for month in range(1, 13):
                        variation = (hash(f"{crop}{state}{year}{month}") % 500) - 250
                        data.append({
                            "Crop": crop,
                            "State": state,
                            "Year": year,
                            "Month": month,
                            "Price_per_Quintal": base_price + variation + (year - 2013) * 100
                        })
        
        return pd.DataFrame(data)
    
    async def load_initial_datasets(self):
        """Load all datasets initially"""
        logger.info("Loading initial datasets...")
        tasks = [self.fetch_dataset(key) for key in self.DATASETS.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for key, result in zip(self.DATASETS.keys(), results):
            if isinstance(result, Exception):
                logger.error(f"Failed to load {key}: {result}")
            else:
                logger.info(f"Loaded {key}: {len(result)} rows")
    
    async def get_dataset_info(self, dataset_key: str) -> Dict[str, Any]:
        """Get information about a dataset"""
        if dataset_key not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset_key}")
        
        info = self.DATASETS[dataset_key].copy()
        
        # Try to load dataset to get additional info
        try:
            df = await self.fetch_dataset(dataset_key)
            info["row_count"] = len(df)
            info["columns"] = list(df.columns)
            info["last_cached"] = datetime.fromtimestamp(
                self._get_cache_path(dataset_key).stat().st_mtime
            ).isoformat()
        except Exception as e:
            logger.warning(f"Could not get dataset info: {e}")
        
        return info
    
    async def query_dataset(
        self,
        dataset_key: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Query a dataset with filters
        
        Args:
            dataset_key: Dataset to query
            filters: Dict of column -> value filters
            limit: Maximum rows to return
        """
        df = await self.fetch_dataset(dataset_key)
        
        # Apply filters
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    if isinstance(value, list):
                        df = df[df[column].isin(value)]
                    else:
                        df = df[df[column] == value]
        
        return df.head(limit)
    
    async def close(self):
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
