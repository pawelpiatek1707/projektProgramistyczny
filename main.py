import base64
import glob
import io
import os
from datetime import datetime, date
import cv2
from PIL import Image
from flask import Flask, render_template, Response, jsonify, make_response, request


app = Flask(__name__)
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}
camera = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6

upload_directory = 'static/images'


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
    saved_image.save(f"static/{file_name}.png")


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


@app.route('/cctv')
def cctv():
    today = date.today()
    print(today)
    return render_template('index.html', date=today)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/images')
def test():
    basic_token = request.headers['Authorization'].split(' ')[1]
    if basic_token == 'cHJvamVrdDpwcm9ncmFtaXN0eWN6bnk=':
        files = []
        for file in glob.glob('static/*.png'):
            name = file.split('\\')[1].split('.')[0]
            img = Image.open(file, mode='r')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('utf-8').replace('\n', '')
            response_data = {"name": name, "image": my_encoded_img}
            files.append(response_data)
        response = jsonify(files)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        message = 'Failed to delete image'
        response = jsonify({"message": message})
        return response, 500



# @app.route('/images/<name>')
# def get_image(name):
#     filename = f"static/{name}.png"
#     img = Image.open(filename, mode='r')
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format='PNG')
#     my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('utf-8').replace('\n', '')
#     response_data = {"name": name, "image": my_encoded_img}
#
#     return jsonify(response_data)


@app.route('/images/<name>', methods=['DELETE'])
def del_image(name):
    basic_token = request.headers['Authorization'].split(' ')[1]
    if basic_token == 'cHJvamVrdDpwcm9ncmFtaXN0eWN6bnk=':
        file_path = f"static/{name}.png"
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")

        try:
            os.remove(file_path)
            message = 'Image deleted successfully'
            response = jsonify({"message": message})
            return response, 200
        except OSError:
            message = 'Failed to delete image'
            response = jsonify({"message": message})
            return response, 500
    else:
        message = 'Failed to delete image'
        response = jsonify({"message": message})
        return response, 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] and data['password']:
        basic_token = base64.b64encode(bytes(f"{data['username']}:{data['password']}", "utf-8")).decode("ascii")
        message = 'Image deleted successfully'
        response = jsonify({"message": message, "basic": basic_token})
        return response, 200
    else:
        message = 'Failed to delete image'
        response = jsonify({"message": message})
        return response, 500


if __name__ == "__main__":
    app.run(debug=True)
