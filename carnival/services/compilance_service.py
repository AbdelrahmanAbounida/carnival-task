from carnival.services.optimization_service import (
    OptimizationResult,
    OptimizationService,
)
from carnival.services.route_service import RegionFuels, RouteService
from carnival.services.base import Service
from pydantic import BaseModel
from typing import Awaitable


class CompliantReport(BaseModel):
    is_compliant: bool
    non_compliant_entries: list[dict]  # TODO:: add fixed schema


class ComplianceService(Service):
    def __init__(
        self, optimization_service: OptimizationService, route_service: RouteService
    ):
        self.optimization_service = optimization_service
        self.route_service = route_service

    async def check_optimization_compliance(
        self, departure_port: str, arrival_port: str
    ) -> Awaitable[CompliantReport]:
        """generate compilant report for the optimization data generated for a sepcific ship route between 2 ports"""
        optimization_result = (
            await self.optimization_service.get_and_cache_optimization_results(
                departure_port, arrival_port
            )
        )
        allowed_fuels = await self.route_service.get_allowed_fuels(
            departure_port, arrival_port
        )

        compliance_report = self._check_compliance(optimization_result, allowed_fuels)
        return compliance_report

    def _check_compliance(
        self, optimization_result: list[OptimizationResult], allowed_fuels: RegionFuels
    ) -> CompliantReport:
        non_compliant_entries = []

        for entry in optimization_result:
            latitude, longitude = entry.latitude, entry.longitude
            used_fuel = "HFO" if entry.hfo_fuel_consumption > 0 else "MGO"

            for region in allowed_fuels.regions:
                if region.region_start <= latitude <= region.region_end:
                    if used_fuel not in region.is_aaqs_allowed:
                        non_compliant_entries.append(
                            {
                                "timestamp": entry.timestamp,
                                "latitude": latitude,
                                "longitude": longitude,
                                "used_fuel": used_fuel,
                                "allowed_fuels": region.is_aaqs_allowed,
                            }
                        )
                    break

        return CompliantReport(
            is_compliant=len(non_compliant_entries) == 0,
            non_compliant_entries=non_compliant_entries,
        )
