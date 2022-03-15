from flask import Flask, render_template, Response
import cv2
from datetime import datetime
from PIL import Image

app = Flask(__name__)
camera = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


def get_frames():
    ret, frame = camera.read()

    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
                       interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in face_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break
    ret, jpeg = cv2.imencode('.jpg', frame)
    has_face = len(face_rects) > 0
    return jpeg.tobytes(), has_face, frame


def capture_image(img):
    date = str(datetime.timestamp(datetime.now()))
    file_name = date.replace(".", "_")
    saved_image = Image.fromarray(img, 'RGB')
    saved_image.save(f"images/{file_name}.png")


def calculate_time_difference(base_time):
    current_time = datetime.now()
    time_difference = (current_time - base_time).total_seconds()
    return time_difference


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def test():
    return 'test'


if __name__ == "__main__":
    app.run(debug=True)
