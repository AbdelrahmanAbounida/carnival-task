from unittest.mock import patch

import pytest
from pandas import DataFrame

from carnival.exceptions import (
    OptimizationResultsNotFoundException,
    OptimizationResultsNotValidException,
)
from carnival.services.optimization_service import (
    OptimizationResult,
    OptimizationService,
)


@pytest.mark.data_validation
def test_valid_dataframe_schema(
    optimization_service: OptimizationService, correct_mock_dataframe: DataFrame
):
    """Test validation of correct dataframe schema"""
    with patch.object(OptimizationResult, "__init__", return_value=None):
        results = optimization_service._serialize_results_schema(correct_mock_dataframe)
        assert isinstance(results, list)
        assert len(results) == 4
        assert all(isinstance(item, OptimizationResult) for item in results)


@pytest.mark.data_validation
def test_wrong_results_serialization(
    optimization_service: OptimizationService, wrong_mock_dataframe
):
    """Test validation fails when required columns are missing"""
    with pytest.raises(OptimizationResultsNotValidException):
        optimization_service._serialize_results_schema(wrong_mock_dataframe)


def test_results_serialization(
    optimization_service: OptimizationService, correct_mock_dataframe: DataFrame
):
    """Test the complete serialization process"""
    with patch.object(OptimizationResult, "__init__", return_value=None):
        results = optimization_service._serialize_results_schema(correct_mock_dataframe)
        assert len(results) == len(correct_mock_dataframe)
        assert all(isinstance(result, OptimizationResult) for result in results)


@pytest.mark.asyncio
async def test_invalid_ports_optimization(
    optimization_service: OptimizationService,
    correct_mock_dataframe: DataFrame,
):
    """Test raising error when invalid ports are passed to the optimization service"""
    with patch.object(
        optimization_service, "_serialize_results_schema"
    ) as mock_serialize:
        mock_serialize.return_value = [
            OptimizationResult(**row)
            for row in correct_mock_dataframe.to_dict("records")
        ]

        with pytest.raises(OptimizationResultsNotFoundException):
            await optimization_service.get_and_cache_optimization_results(
                "PORT1",
                "PORT2",
            )


@pytest.mark.asyncio
async def test_valid_ports_optimization(
    optimization_service: OptimizationService, correct_mock_dataframe: DataFrame
):
    with patch.object(
        optimization_service, "_serialize_results_schema"
    ) as mock_serialize:
        mock_serialize.return_value = [
            OptimizationResult(**row)
            for row in correct_mock_dataframe.to_dict("records")
        ]

        results = await optimization_service.get_and_cache_optimization_results(
            "OMSTQ",
            "AEJEA",
        )
        assert len(results) == len(correct_mock_dataframe)
        assert all(isinstance(result, OptimizationResult) for result in results)


# TODO:: test caching
