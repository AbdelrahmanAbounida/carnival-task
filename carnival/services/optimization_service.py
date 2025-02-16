import os
from datetime import datetime
from functools import lru_cache
from io import StringIO
from typing import Awaitable

import aiofiles
import pandas as pd
from pandas import DataFrame
from pydantic import BaseModel

from carnival.core.config import settings
from carnival.core.logger import logger
from carnival.exceptions import (
    OptimizationResultsFileReadException,
    OptimizationResultsNotFoundException,
    OptimizationResultsNotValidException,
)
from carnival.services.base import Service


class OptimizationResult(BaseModel):
    timestamp: datetime
    sog: float
    latitude: float
    longitude: float
    timezone_name: str
    hfo_fuel_consumption: float
    mgo_fuel_consumption: float
    avg_rpm: float
    mgo_fuel_flow_tonnes_per_h: float
    hfo_fuel_flow_tonnes_per_h: float
    sulphur_content: float

    class ConfigDict:
        populate_by_name = True


class OptimizationService(Service):
    def __init__(self, efs_storage_path: str = None):
        self.efs_storage_path = (
            efs_storage_path or settings.OPTIMIZATION_SERVICE_BASE_FILE
        )

    @lru_cache(
        10
    )  # Assuming EFS Service might need cache (testing could prove the reverse)
    async def get_and_cache_optimization_results(
        self, departure_port: str, arrival_port: str, force_reload: bool = False
    ) -> Awaitable[list[OptimizationResult]]:
        """generate optimization results based on the given ports and load data from according file

        Note: Lets assume that the optimization result store its response in a file format like
        optimization_{departure_port}_{arrival_port}.csv >> so we can load it from the EFS storage

        """
        if force_reload:
            self.get_and_cache_optimization_results.cache_clear()

        # 1- check optimization results file
        optimization_file_path = self._get_optimization_file_path(
            departure_port, arrival_port
        )

        # 2- load optimization results from file
        optimization_results = await self._load_optimization_file_results(
            optimization_file_path
        )

        # 3- validate results schema
        serialized_optimization_resulst = self._serialize_results_schema(
            optimization_results
        )

        return serialized_optimization_resulst

    def _get_optimization_file_path(self, departure_port: str, arrival_port: str):
        file_path = (
            f"{self.efs_storage_path}/optimization_{departure_port}_{arrival_port}.csv"
        )

        if not os.path.exists(file_path):
            logger.error(f"OPTIMIZATION_SERVICE:: {file_path} NOT exist ")
            raise OptimizationResultsNotFoundException(
                departure_port=departure_port, arrival_port=arrival_port
            )

        return file_path

    async def _load_optimization_file_results(self, file_path: str) -> pd.DataFrame:
        """get an optimization file and read its content"""
        try:
            async with aiofiles.open(file_path, mode="r") as f:
                content = await f.read()
            df = pd.read_csv(StringIO(content))
            return df
        except Exception as e:
            logger.error(f"OPTIMIZATION_SERVICE: failed to load EFS File >> \n {e}")
            raise OptimizationResultsFileReadException("Failed to read EFS File")

    def _serialize_results_schema(
        self, optimization_results: DataFrame
    ) -> list[OptimizationResult]:
        """to validate the optimization schema columns"""
        try:
            df_dict = optimization_results.to_dict(orient="records")
            serialized_results = [OptimizationResult(**row) for row in df_dict]
            logger.success(
                "OPTIMIZATION SERVICE:: optimization results schema is valid"
            )
            return serialized_results
        except Exception as e:
            logger.error(
                f"OPTIMIZATION SERVICE:: failed to validate optimization resutls schema >> \n {e}"
            )
            raise OptimizationResultsNotValidException("Optimization results not valid")
