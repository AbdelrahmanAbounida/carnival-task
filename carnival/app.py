from fastapi import FastAPI, Depends
from carnival.api.router import router
from carnival.core.auth import get_static_api_key
from fastapi.middleware.cors import CORSMiddleware

StaticAPIKey = Depends(get_static_api_key)
app: FastAPI = FastAPI(
    dependencies=[StaticAPIKey],
)

## Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
async def root_route() -> dict[str, str]:
    return {"message": " Compilance Service API Server is running"}


app.include_router(router)
