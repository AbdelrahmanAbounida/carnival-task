from fastapi import FastAPI

app: FastAPI = FastAPI()
# TODO:: add route handlers, middleware , lifespan


@app.get("/", tags=["Home"])
async def root_route() -> dict[str, str]:
    return {"message": " Compilance Service API Server is running"}
