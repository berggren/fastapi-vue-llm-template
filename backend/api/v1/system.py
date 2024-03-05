from fastapi import APIRouter
from api.config import config


router = APIRouter()


@router.get("/config")
def get_config():
    llms = config.get("llms", [])
    active_llms = [
        service for service in llms.values() if service.get("enabled", False)
    ]
    return {"active_llms": active_llms}
