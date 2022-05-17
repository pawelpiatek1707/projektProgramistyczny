from datetime import datetime
from PIL import Image


def capture_image(img):
    date = str(datetime.timestamp(datetime.now()))
    file_name = date.replace(".", "_")
    saved_image = Image.fromarray(img, 'RGB')
    saved_image.save(f"static/{file_name}.png")