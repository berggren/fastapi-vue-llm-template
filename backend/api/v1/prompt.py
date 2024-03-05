from pydantic import BaseModel
from fastapi import APIRouter
from api.plugins.llms import manager

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    provider: str


class PromptResponse(BaseModel):
    response: str


@router.post("/generate")
async def generate(request: PromptRequest):
    provider = manager.LLMManager().get_provider(request.provider)()
    response = provider.generate(request.prompt)
    return PromptResponse(response=response)
