import time
import base64
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from ..model.schemes import SegmentationRequest
from ..controllers.seg_controller import preprocess, predict, build_overlay, compute_stats
from ..model.schemes import SegmentationResponse
from ..util.config import Config
from ..util.utility import numpy_to_b64
from ..model.enums.enums import segmentationEnums


config = Config()
seg_router = APIRouter(prefix='/api/v1/segmentation')

@seg_router.post('/')
async def segment_image(request: Request, body: SegmentationRequest):
    try:
        image_bytes = base64.b64decode(body.image_b64)
    except Exception:
        return JSONResponse(
            status_code=422,
            content = {
                'signal' : segmentationEnums.INVALID_IMAGE.value
            }
        )

    if len(image_bytes) == 0:
        return JSONResponse(
            status_code=400,
            content = {
                'signal' : segmentationEnums.IMAGE_EMPTY.value
            }
        )

    if len(image_bytes) > config.max_file_size:
        return JSONResponse(
            status_code=413,
            content = {
                'signal' : f"{segmentationEnums.IMAGE_TOO_LARGE.value} ({len(image_bytes) / 1e6:.1f} MB). Maximum allowed size is {config.max_file_size / 1e6:.1f} MB."
            }
        )

    try:
        image_rgb, image_resized, tensor = preprocess(image_bytes)
    except ValueError as e:
        return JSONResponse(
            status_code=422,
            content = {
                'signal' : str(e)
            }
        )
    
    t0 = time.perf_counter()
    prob_map, pred_mask = predict(request.app.state.model, tensor)
    inference_ms = round((time.perf_counter() - t0) * 1000, 2)

    overlay = build_overlay(image_resized, pred_mask)
    stats = compute_stats(pred_mask)

    return SegmentationResponse(
        ulcer_detected = stats["ulcer_detected"],
        ulcer_pixels   = stats["ulcer_pixels"],
        total_pixels   = stats["total_pixels"],
        ulcer_coverage = stats["ulcer_coverage"],
        inference_ms   = inference_ms,
        mask_b64       = numpy_to_b64(pred_mask, is_mask=True),
        overlay_b64    = numpy_to_b64(overlay,   is_mask=False),
    )


