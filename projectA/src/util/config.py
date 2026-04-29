from pydantic import BaseModel, ConfigDict
from util.utility import get_device
import numpy as np
import torch

class Config(BaseModel):
    model_path: str = "model/unet.pth"
    device: torch.device = get_device()

    feature_channels: list[int] = [64, 128, 256, 512]
    input_channels: int = 3
    output_channels: int = 1
    
    img_size: int = 512
    threshold: float = 0.5

    mean: np.ndarray = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std: np.ndarray = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    max_file_size: int = 20 * 1024 * 1024  # 20 MB
    min_image_dim: int = 64

    model_config = ConfigDict(arbitrary_types_allowed=True)

config = Config()