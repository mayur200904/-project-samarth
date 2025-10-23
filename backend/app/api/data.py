"""
Data API endpoints
"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional, List
import logging

from app.models.schemas import DatasetInfo, DataQuery, DataQueryResponse, DataSource

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/datasets", response_model=List[DatasetInfo])
async def list_datasets(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category (agriculture, climate)")
):
    """
    List all available datasets
    """
    try:
        data_fetcher = request.app.state.data_fetcher
        
        datasets = []
        for key, info in data_fetcher.DATASETS.items():
            # Filter by category if specified
            if category and info.get("category") != category:
                continue
            
            try:
                # Get additional info
                dataset_info = await data_fetcher.get_dataset_info(key)
                
                datasets.append(DatasetInfo(
                    dataset_id=key,
                    name=info["name"],
                    description=info["description"],
                    organization=info["category"],
                    category=info["category"],
                    format="parquet",
                    fields=dataset_info.get("columns", []),
                    row_count=dataset_info.get("row_count"),
                    last_updated=dataset_info.get("last_cached", ""),
                    url=info["url"],
                    tags=[info["category"]]
                ))
            except Exception as e:
                logger.warning(f"Failed to get info for {key}: {e}")
        
        return datasets
        
    except Exception as e:
        logger.error(f"List datasets error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_id}", response_model=DatasetInfo)
async def get_dataset(dataset_id: str, request: Request):
    """
    Get detailed information about a specific dataset
    """
    try:
        data_fetcher = request.app.state.data_fetcher
        
        if dataset_id not in data_fetcher.DATASETS:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        info = data_fetcher.DATASETS[dataset_id]
        dataset_info = await data_fetcher.get_dataset_info(dataset_id)
        
        return DatasetInfo(
            dataset_id=dataset_id,
            name=info["name"],
            description=info["description"],
            organization=info["category"],
            category=info["category"],
            format="parquet",
            fields=dataset_info.get("columns", []),
            row_count=dataset_info.get("row_count"),
            last_updated=dataset_info.get("last_cached", ""),
            url=info["url"],
            tags=[info["category"]]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get dataset error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/datasets/query", response_model=DataQueryResponse)
async def query_dataset(query: DataQuery, request: Request):
    """
    Query a dataset with filters
    """
    try:
        data_fetcher = request.app.state.data_fetcher
        
        if query.dataset_id not in data_fetcher.DATASETS:
            raise HTTPException(status_code=404, detail=f"Dataset {query.dataset_id} not found")
        
        # Query the dataset
        df = await data_fetcher.query_dataset(
            dataset_key=query.dataset_id,
            filters=query.filters,
            limit=query.limit
        )
        
        # Get dataset info
        info = data_fetcher.DATASETS[query.dataset_id]
        dataset_info = await data_fetcher.get_dataset_info(query.dataset_id)
        
        metadata = DatasetInfo(
            dataset_id=query.dataset_id,
            name=info["name"],
            description=info["description"],
            organization=info["category"],
            category=info["category"],
            format="parquet",
            fields=dataset_info.get("columns", []),
            row_count=dataset_info.get("row_count"),
            last_updated=dataset_info.get("last_cached", ""),
            url=info["url"],
            tags=[info["category"]]
        )
        
        # Convert dataframe to records
        data = df.to_dict(orient="records")
        
        return DataQueryResponse(
            dataset_id=query.dataset_id,
            data=data,
            total_count=dataset_info.get("row_count", len(data)),
            returned_count=len(data),
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query dataset error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/datasets/{dataset_id}/refresh")
async def refresh_dataset(dataset_id: str, request: Request):
    """
    Refresh a dataset from the API
    """
    try:
        data_fetcher = request.app.state.data_fetcher
        
        if dataset_id not in data_fetcher.DATASETS:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} not found")
        
        # Force refresh
        df = await data_fetcher.fetch_dataset(dataset_id, force_refresh=True)
        
        return {
            "dataset_id": dataset_id,
            "status": "refreshed",
            "row_count": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Refresh dataset error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
