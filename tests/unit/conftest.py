from io import StringIO

import pandas as pd
import pytest
from carnival.core.config import settings
from carnival.services.optimization_service import (
    OptimizationResult,
    OptimizationService,
)
from carnival.services.route_service import AllowedRegionFuel, RegionFuels, RouteService
from carnival.services.compilance_service import ComplianceService
from unittest.mock import MagicMock


@pytest.fixture
def correct_dep_port():
    return "OMSTQ"


@pytest.fixture
def correct_arrival_port():
    return "AEJEA"


# ************************
# Optimization Service
# ************************

# Optimization service mock data
MOCK_CORRECT_CSV_CONTENT = """
timestamp,sog,latitude,longitude,timezone_name,hfo_fuel_consumption,mgo_fuel_consumption,avg_rpm,mgo_fuel_flow_tonnes_per_h,hfo_fuel_flow_tonnes_per_h,sulphur_content
2025-02-04 01:30:00,8.74,23.76539,58.51709,Asia/Muscat,0.0,1.72,47.94,1.72,0.0,0.1
2025-02-04 02:00:00,7.9,23.83227,58.46255,Asia/Muscat,0.0,1.68,44.82,1.68,0.0,0.1
2025-02-04 02:30:00,7.62,23.89916,58.40801,Asia/Muscat,0.0,1.68,44.73,1.68,0.0,0.1
2025-02-04 03:00:00,7.46,23.96605,58.35345,Asia/Muscat,0.0,1.7,44.59,1.7,0.0,0.1
"""

# Mock data for testing
MOCK_WRONG_CSV_CONTENT = """
column1,column2,column3
value1,value2,value3
value4,value5,value6
"""


@pytest.fixture
def optimization_service():
    return OptimizationService(efs_storage_path=settings.OPTIMIZATION_SERVICE_BASE_FILE)


@pytest.fixture
def correct_mock_dataframe():
    return pd.read_csv(StringIO(MOCK_CORRECT_CSV_CONTENT.strip()))


@pytest.fixture
def wrong_mock_dataframe():
    return pd.read_csv(StringIO(MOCK_WRONG_CSV_CONTENT.strip()))


# ************************
# Route Service
# ************************

# Route service mock data
MOCK_ALLOWED_FUELS = {
    "regions": [
        {
            "region_start": 0.0,
            "region_end": 27.140542199038926,
            "is_aaqs_allowed": ["MGO"],
        },
        {
            "region_start": 27.140542199038926,
            "region_end": 189.17802962860196,
            "is_aaqs_allowed": ["MGO", "HFO"],
        },
    ]
}

MOCK_ROUTE_GEOMETRY = {
    "type": "LineString",
    "coordinates": [[58.567496, 23.628134], [58.57067786645131, 23.626216028496188]],
}


@pytest.fixture
def route_service():
    return RouteService(base_file_path=settings.ROUTE_SERVICE_BASE_FILE)


@pytest.fixture
def mock_route_geometry():
    return MOCK_ROUTE_GEOMETRY


@pytest.fixture
def mock_allowed_fuels():
    return MOCK_ALLOWED_FUELS


# ************************
# Compilance Service
# ************************


@pytest.fixture
def compliance_service():
    optimization_service = MagicMock()
    route_service = MagicMock()
    return ComplianceService(optimization_service, route_service)


@pytest.fixture
def allowed_fuels():
    return RegionFuels(
        regions=[
            AllowedRegionFuel(
                region_start=0.0, region_end=27.0, is_aaqs_allowed=["MGO"]
            )
        ]
    )


@pytest.fixture
def wrong_allowed_fuels():
    return RegionFuels(
        regions=[
            AllowedRegionFuel(
                region_start=0.0, region_end=27.0, is_aaqs_allowed=["MGO"]
            )
        ]
    )


@pytest.fixture
def optimization_result():
    return [
        OptimizationResult(
            timestamp="2025-02-04 01:30:00",
            sog=10.5,
            latitude=23.7,
            longitude=58.5,
            timezone_name="UTC",
            hfo_fuel_consumption=0.0,
            mgo_fuel_consumption=1.72,
            avg_rpm=150,
            mgo_fuel_flow_tonnes_per_h=0.05,
            hfo_fuel_flow_tonnes_per_h=0.1,
            sulphur_content=0.5,
        ),
        OptimizationResult(
            timestamp="2025-02-04 02:00:00",
            sog=11.0,
            latitude=23.8,
            longitude=58.4,
            timezone_name="UTC",
            hfo_fuel_consumption=0.0,
            mgo_fuel_consumption=1.68,
            avg_rpm=155,
            mgo_fuel_flow_tonnes_per_h=0.04,
            hfo_fuel_flow_tonnes_per_h=0.09,
            sulphur_content=0.5,
        ),
    ]


@pytest.fixture
def wrong_optimization_result():
    return [
        OptimizationResult(
            timestamp="2025-02-04 01:30:00",
            sog=10.5,
            latitude=23.7,
            longitude=58.5,
            timezone_name="UTC",
            hfo_fuel_consumption=1.5,
            mgo_fuel_consumption=0.0,
            avg_rpm=150,
            mgo_fuel_flow_tonnes_per_h=0.05,
            hfo_fuel_flow_tonnes_per_h=0.1,
            sulphur_content=0.5,
        ),
        OptimizationResult(
            timestamp="2025-02-04 02:00:00",
            sog=11.0,
            latitude=23.8,
            longitude=58.4,
            timezone_name="UTC",
            hfo_fuel_consumption=1.2,
            mgo_fuel_consumption=0.0,
            avg_rpm=155,
            mgo_fuel_flow_tonnes_per_h=0.04,
            hfo_fuel_flow_tonnes_per_h=0.09,
            sulphur_content=0.5,
        ),
    ]
