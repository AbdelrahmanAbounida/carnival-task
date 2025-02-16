# *************************
# Optimization Service
# *************************


class OptimizationResultsNotFoundException(Exception):
    """Exception raised when optimization results are not found."""

    def __init__(self, departure_port: str, arrival_port: str, message: str = None):
        self.departure_port = departure_port
        self.arrival_port = arrival_port
        self.message = (
            message
            or f"Optimization results not found for route from {departure_port} to {arrival_port}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

    def __repr__(self):
        return f"OptimizationResultsNotFoundException({self.departure_port!r}, {self.arrival_port!r}, {self.message!r})"


class OptimizationResultsNotValidException(Exception):
    pass


class OptimizationResultsFileReadException(Exception):
    pass


# *************************
# Route Service
# *************************


class RouteNotFoundException(Exception):
    """raise this exception in case no route found between 2 ports"""
