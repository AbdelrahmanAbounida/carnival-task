"""
Main Router for different API Versions
"""

from fastapi import APIRouter
from carnival.api.v1.compilance import router as compilance_router
from carnival.core.config import settings
from carnival.api.health_check import router as health_check_router

# *****************
# Version1 Routes
# *****************

router = APIRouter(prefix=f"/api/{settings.CURRENT_VERSION}")

router.include_router(compilance_router)
router.include_router(health_check_router)
