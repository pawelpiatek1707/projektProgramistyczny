import base64
import glob
import io
import os
from datetime import date
from PIL import Image
from flask import Flask, render_template, Response, jsonify, make_response, request
from helpers.generate_frames import generate_frames


app = Flask(__name__)

upload_directory = 'static/images'


@app.route('/')
def cctv():
    today = date.today()
    print(today)
    return render_template('index.html', date=today)


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
