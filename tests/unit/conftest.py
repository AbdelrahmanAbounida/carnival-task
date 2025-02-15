from io import StringIO

import pandas as pd
import pytest

from carnival.core.config import settings
from carnival.services.optimization_service import OptimizationService

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
