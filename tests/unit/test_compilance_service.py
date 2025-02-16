from carnival.services.compilance_service import ComplianceService
from carnival.services.optimization_service import OptimizationResult
from carnival.services.route_service import RegionFuels
import pytest


@pytest.mark.asyncio
async def test_compliance_allows_correct_fuel(
    compliance_service: ComplianceService,
    optimization_result: list[OptimizationResult],
    allowed_fuels: RegionFuels,
    correct_dep_port,
    correct_arrival_port,
):
    # Mock the method properly
    compliance_service.optimization_service.get_and_cache_optimization_results.return_value = optimization_result
    compliance_service.route_service.get_allowed_fuels.return_value = allowed_fuels

    report = await compliance_service.check_optimization_compliance(
        correct_dep_port, correct_arrival_port
    )
    assert report.is_compliant
    assert len(report.non_compliant_entries) == 0


@pytest.mark.asyncio
async def test_compliance_detects_wrong_fuel(
    compliance_service: ComplianceService,
    wrong_optimization_result: list[OptimizationResult],
    wrong_allowed_fuels: RegionFuels,
    correct_dep_port,
    correct_arrival_port,
):
    compliance_service.optimization_service.get_and_cache_optimization_results.return_value = wrong_optimization_result
    compliance_service.route_service.get_allowed_fuels.return_value = (
        wrong_allowed_fuels
    )

    report = await compliance_service.check_optimization_compliance(
        correct_dep_port, correct_arrival_port
    )
    assert not report.is_compliant
    assert len(report.non_compliant_entries) == 2
