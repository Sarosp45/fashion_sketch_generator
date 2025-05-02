import os
from datetime import datetime
from utils.logger import *
def save_image(content, prefix="generated"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)

    with open(path, "wb") as f:
        f.write(content)
    eval_logger.info("Image Generated")
    return path
