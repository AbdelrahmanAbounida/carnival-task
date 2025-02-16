from pydantic import BaseModel


class CheckCompilancePayload(BaseModel):
    departure_port: str
    arrival_port: str
