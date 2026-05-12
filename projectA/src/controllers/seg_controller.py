import cv2
import numpy as np
import torch
from pathlib import Path

from ..model.unet import UNet
from ..util.utility import get_device
from ..util.config import Config
from ..util.utility import decode_image_bytes 

config = Config()

def load_model(model_path: str = config.model_path) -> UNet:
    if not Path(model_path).exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {model_path}\n"
            f"Place unet.pth in the project root."
        )
    model = UNet(in_channels=config.input_channels,
                 out_channels=config.output_channels,
                 features=config.feature_channels)
    model.load_state_dict(torch.load(model_path, map_location=config.device))
    model.to(config.device)
    model.eval()
    print(f"Diabetic foot ulcer model loaded on {config.device}")
    return model


def preprocess(image_bytes: bytes) -> tuple[np.ndarray, np.ndarray, torch.Tensor]:
    image_rgb = decode_image_bytes(image_bytes)

    h, w = image_rgb.shape[:2]
    if h < config.min_image_dim or w < config.min_image_dim:
        raise ValueError(
            f"Image too small ({w}×{h}). "
            f"Please upload a clear smartphone photo of the foot."
        )

    image_resized = cv2.resize(image_rgb, (config.img_size, config.img_size), interpolation=cv2.INTER_LINEAR)
    normalized = (image_resized.astype(np.float32) / 255.0 - config.mean) / config.std
    tensor = torch.from_numpy(normalized.transpose(2, 0, 1)).unsqueeze(0).to(config.device)

    return image_rgb, image_resized, tensor


def predict(model: UNet, tensor: torch.Tensor) -> tuple[np.ndarray, np.ndarray]:
    with torch.inference_mode():
        logits = model(tensor)
        prob   = torch.sigmoid(logits).squeeze().cpu().numpy().astype(np.float32)
    pred_mask = (prob >= config.threshold).astype(np.uint8)
    return prob, pred_mask


def build_overlay(image_resized: np.ndarray, pred_mask: np.ndarray) -> np.ndarray:
    overlay = image_resized.copy().astype(np.float32) / 255.0
    if pred_mask.max() > 0:
        overlay[pred_mask == 1] = (
            overlay[pred_mask == 1] * 0.45 +
            np.array([1.0, 0.15, 0.1]) * 0.55
        )
    return (overlay * 255).clip(0, 255).astype(np.uint8)


def compute_stats(pred_mask: np.ndarray) -> dict:
    total_pixels = pred_mask.size
    ulcer_pixels = int(pred_mask.sum())
    return {
        "ulcer_detected" : ulcer_pixels > 0,
        "ulcer_pixels" : ulcer_pixels,
        "total_pixels" : total_pixels,
        "ulcer_coverage" : round(100.0 * ulcer_pixels / total_pixels, 4),
    }