from locust import HttpUser, task, constant_pacing
from dotenv import load_dotenv
import os

load_dotenv()


class ComplianceTestUser(HttpUser):
    wait_time = constant_pacing(1)  # 1 sec between requests

    @task
    def check_compliance_route(self):
        params = {"departure_port": "OMSTQ", "arrival_port": "AEJEA"}
        headers = {"server-api-key": os.environ.get("SERVER_API_KEY")}
        self.client.get("/api/v1/compilance", params=params, headers=headers)
