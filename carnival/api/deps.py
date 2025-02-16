from carnival.services.optimization_service import OptimizationService
from carnival.services.route_service import RouteService
from carnival.services.compilance_service import ComplianceService


# TODO >> could be moved to a service registery / manager
optimiztion_service = None
route_service = None
compilance_service = None


def get_optimization_service():
    global optimiztion_service
    if not optimiztion_service:
        optimiztion_service = OptimizationService()
    return optimiztion_service


def get_route_service():
    global route_service
    if not route_service:
        route_service = RouteService()
    return route_service


def get_compilance_service():
    global compilance_service
    if not compilance_service:
        compilance_service = ComplianceService(
            get_optimization_service(), get_route_service()
        )
    return compilance_service
