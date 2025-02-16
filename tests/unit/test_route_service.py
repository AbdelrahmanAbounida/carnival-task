import pytest
from unittest.mock import patch
from carnival.exceptions import RouteNotFoundException
from carnival.services.route_service import RouteService, RouteGeometry, RegionFuels


# Mock data for the RouteGeometry and RegionFuels
@pytest.fixture
def mock_route_geometry():
    return {
        "type": "LineString",
        "coordinates": [
            [58.567496, 23.628134],
            [58.57067786645131, 23.626216028496188],
        ],
    }


@pytest.fixture
def mock_allowed_fuels():
    return {
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


@pytest.mark.asyncio
async def test_get_route_geometry_success(
    route_service: RouteService, mock_route_geometry
):
    # Patch the method to mock the return value
    with patch.object(
        route_service,
        "get_route_geometry",
        return_value=RouteGeometry(**mock_route_geometry),
    ):
        result = await route_service.get_route_geometry("OMSTQ", "AEJEA")

    # Assert the result is a RouteGeometry object
    assert isinstance(result, RouteGeometry)
    assert isinstance(result.coordinates, list)
    assert len(result.coordinates) > 0  # Ensure there are coordinates


@pytest.mark.asyncio
async def test_get_allowed_fuels_success(
    route_service: RouteService, mock_allowed_fuels
):
    # Patch the method to mock the return value
    with patch.object(
        route_service,
        "get_allowed_fuels",
        return_value=RegionFuels(**mock_allowed_fuels),
    ):
        result = await route_service.get_allowed_fuels("OMSTQ", "AEJEA")

    # Assert the result is a RegionFuels object
    assert isinstance(result, RegionFuels)
    assert len(result.regions) == 2
    assert result.regions[0].region_start == 0.0
    assert result.regions[1].is_aaqs_allowed == ["MGO", "HFO"]


@pytest.mark.asyncio
async def test_get_route_geometry_ports_not_found(route_service: RouteService):
    # Simulate a file not found error
    with patch("aiofiles.open", side_effect=FileNotFoundError):
        with pytest.raises(RouteNotFoundException):
            await route_service.get_route_geometry("NYC", "LA")


@pytest.mark.asyncio
async def test_get_allowed_fuels_ports_not_found(route_service: RouteService):
    # Simulate a file not found error
    with patch("aiofiles.open", side_effect=FileNotFoundError):
        with pytest.raises(RouteNotFoundException):
            await route_service.get_allowed_fuels("NYC", "LA")
