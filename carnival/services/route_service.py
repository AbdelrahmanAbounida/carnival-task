from carnival.exceptions import RouteNotFoundException
from carnival.services.base import Service
from carnival.core.config import settings
from carnival.core.logger import logger
from pydantic import BaseModel
from typing import Awaitable
import json
import aiofiles
import os


class RouteGeometry(BaseModel):
    type: str
    coordinates: list[list[float]]


class AllowedRegionFuel(BaseModel):
    region_start: float
    region_end: float
    is_aaqs_allowed: list[str]


class RegionFuels(BaseModel):
    regions: list[AllowedRegionFuel]


class RouteService(Service):
    """This service provides some required information for the compliance service to verify the optimization service

    It does 2 main tasks:

    1. Provides a route geometry for a given departure and arrival port UN locode
    2. Provides information on which fuel is allowed to be used for which region within a certain route.
    """

    def __init__(self, base_file_path: str = None):
        self.base_file_path = base_file_path or settings.ROUTE_SERVICE_BASE_FILE

    async def get_route_geometry(
        self, departure_port_un_locode: str, arrival_port_un_locode: str
    ) -> Awaitable[RouteGeometry]:
        """
        Gets the route geometry between two ports by their UN locodes.

        TODO:: it should be done via httpx call

        Returns:
        - RouteGeometry: The GeoJSON geometry data for the route.
        """
        # 1- get route file path
        route_file_path = self._get_route_file_path(
            departure_port_un_locode, arrival_port_un_locode
        )

        # 2- load file content (as if we call an api)
        async with aiofiles.open(route_file_path, mode="r") as f:
            content = await f.read()

        json_data = json.loads(content)
        return RouteGeometry(**json_data)

    async def get_allowed_fuels(
        self, departure_port_un_locode: str, arrival_port_un_locode: str
    ) -> Awaitable[RegionFuels]:
        """
        Gets the allowed fuels for a route between two ports.

        TODO:: it should be done via httpx call

        Returns:
        - RegionFuels: Information about the allowed fuels within certain regions on the route.
        """
        # 1- get allowed fuels file path
        allowed_fuels_file_path = self._get_allowed_fuels_file_path(
            departure_port_un_locode, arrival_port_un_locode
        )

        # 2- load file content (as if we call an api)
        async with aiofiles.open(allowed_fuels_file_path, mode="r") as f:
            content = await f.read()

        json_data = json.loads(content)
        return RegionFuels(**json_data)

    def _get_route_file_path(
        self, departure_port_un_locode: str, arrival_port_un_locode: str
    ) -> str:
        file_path = f"{self.base_file_path}/route_{departure_port_un_locode}_{arrival_port_un_locode}.json"

        if not os.path.exists(file_path):
            logger.error(
                f"ROUTE_SERVICE: No Geo data found for file path : {file_path}"
            )
            raise RouteNotFoundException(
                f"No Geo data found between ports: {departure_port_un_locode}, {arrival_port_un_locode}"
            )
        return file_path

    def _get_allowed_fuels_file_path(
        self, departure_port_un_locode: str, arrival_port_un_locode: str
    ) -> str:
        file_path = f"{self.base_file_path}/allowed_fuels_{departure_port_un_locode}_{arrival_port_un_locode}.json"

        if not os.path.exists(file_path):
            logger.error(
                f"ROUTE_SERVICE: No allowed fuels data found for file path : {file_path}"
            )
            raise RouteNotFoundException(
                f"No allowed fuels data found between ports: {departure_port_un_locode}, {arrival_port_un_locode}"
            )
        return file_path
