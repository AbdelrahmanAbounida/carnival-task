from locust import HttpUser, task


class CompilantServiceUser(HttpUser):
    @task
    def hello_world(self):
        self.client.post("/api/v1/compilance")
        self.client.get("/world")
