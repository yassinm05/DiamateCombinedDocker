import torch
import numpy as np
import cv2
import base64

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return torch.device("mps") 
    else:
        return torch.device("cpu")
    
def numpy_to_b64(arr: np.ndarray, is_mask: bool = False) -> str:
    if is_mask:
        img = (arr * 255).astype(np.uint8)
        success, buffer = cv2.imencode(".png", img)
    else:
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        success, buffer = cv2.imencode(".png", bgr)

    if not success: 
        raise RuntimeError("Failed to encode image to PNG.")

    return base64.b64encode(buffer).decode("utf-8")


def b64_to_numpy(b64_str: str, is_mask: bool = False) -> np.ndarray:

    raw = base64.b64decode(b64_str)
    arr = np.frombuffer(raw, dtype=np.uint8)

    if is_mask:
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    else:
        bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    return img


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(
            "Could not decode image. Ensure it is a valid JPEG or PNG."
        )
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)