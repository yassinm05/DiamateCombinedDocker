from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.enums.enums import segmentationEnums

base_router = APIRouter()

@base_router.get('/health')
async def health(request: Request):
    model_status = "loaded" if hasattr(request.app.state, "model") else "not loaded"
    if model_status == "not loaded":
        return JSONResponse(
            status_code=503,
            content = {
                'model_loaded' : model_status,
                'device' : "none",
                'signal' : segmentationEnums.MODEL_NOT_LOADED.value
            }
        )
    return JSONResponse(
        status_code=200,
        content = {
            'model_loaded' : model_status,
            'device' : str(next(iter(request.app.state.model.parameters())).device)
                       if hasattr(request.app.state, "model") else "none",
            'signal' : segmentationEnums.MODEL_LOAD_SUCCESS.value
        }
    )