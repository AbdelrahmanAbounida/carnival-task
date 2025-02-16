from fastapi import FastAPI
from carnival.api.router import router

app: FastAPI = FastAPI()
# TODO:: add route handlers, middleware , lifespan


@app.get("/", tags=["Home"])
async def root_route() -> dict[str, str]:
    return {"message": " Compilance Service API Server is running"}


app.include_router(router)
