from services.core.camera import ImgEmotionDetector
from flask import Flask, render_template

import numpy as np
import cv2
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

global imgEmotionDetector
imgEmotionDetector = ImgEmotionDetector()


@app.route('/')
def index():
    return render_template('camcorder.html', data='Emotion Detection Web (A DL4CV Project)!')


def predict_img(frame):
    global imgEmotionDetector
    frame = imgEmotionDetector.get_frame(frame)
    return frame


@socketio.on('image_feed_')
def image_feed_(message):
    filestr = message['data']
    npimg = np.frombuffer(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    ret_val = predict_img(img)
    emit('video_stream', {'data': ret_val})


@socketio.on('connect')
def test_connect():
    emit('message', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
