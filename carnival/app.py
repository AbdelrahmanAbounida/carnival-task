from fastapi import FastAPI, Depends
from carnival.api.router import router
from carnival.core.auth import get_static_api_key
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

StaticAPIKey = Depends(get_static_api_key)
app: FastAPI = FastAPI(
    dependencies=[StaticAPIKey],
)

## CORS Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP Middleware >> compressiong response over 300 byte size with middle level compressing (1-9)
app.add_middleware(GZipMiddleware, minimum_size=300, compresslevel=5)


@app.get("/", tags=["Home"])
async def root_route() -> dict[str, str]:
    return {"message": " Compilance Service API Server is running"}


app.include_router(router)
