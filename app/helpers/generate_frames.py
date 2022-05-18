from datetime import datetime
from app.helpers.get_frames import get_frames
from app.helpers.calculate_time_difference import calculate_time_difference
from app.helpers.capture_image import capture_image


def generate_frames():
    prev_image_date = datetime.min
    print(prev_image_date < datetime.now())

    while True:
        frame, has_face, img = get_frames()
        if has_face:
            time_difference = calculate_time_difference(prev_image_date)
            if time_difference >= 10:
                capture_image(img)
                print('image captured')
                prev_image_date = datetime.now()
        else:
            time_difference = calculate_time_difference(prev_image_date)
            if time_difference >= 10:
                prev_image_date = datetime.min

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')