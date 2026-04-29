from pydantic import BaseModel, Field

class SegmentationRequest(BaseModel):
    image_b64: str = Field(..., description="The image to be segmented, encoded as base64.")

class SegmentationResponse(BaseModel):
    ulcer_detected : bool = Field(..., description="Whether a diabetic foot ulcer was detected")
    ulcer_pixels : int = Field(..., description="Number of pixels classified as ulcer tissue")
    total_pixels : int = Field(..., description="Total pixels in the analysed image")
    ulcer_coverage : float = Field(..., description="Percentage of foot area covered by ulcer (0.0–100.0)")
    inference_ms  : float = Field(..., description="Model inference time in milliseconds")
    mask_b64 : str = Field(..., description="Base64-encoded PNG of binary ulcer mask")
    overlay_b64 : str = Field(..., description="Base64-encoded PNG with ulcer region highlighted")
