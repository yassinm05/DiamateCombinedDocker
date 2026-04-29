from enum import Enum

class segmentationEnums(Enum):
    INVALID_IMAGE = "Invalid image data. Please provide a valid base64-encoded image."
    IMAGE_TOO_LARGE = "Image too large. Maximum allowed size is 20 MB."
    IMAGE_EMPTY = "The image is empty."
    MODEL_NOT_LOADED = "Model is not loaded. Please ensure the model is properly initialized."
    MODEL_LOAD_SUCCESS = "Model is loaded."
