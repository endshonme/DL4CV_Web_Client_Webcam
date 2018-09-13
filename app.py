import services.core.Prediction_CPU as prediction
import services.file_upload_service as file_upload_service
from flask import Flask, send_file, render_template, redirect, flash, request, url_for, jsonify, abort, Response
from json import dumps

app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    return r

@app.route('/')
def index():
    return render_template('index.html', data='Bloomberg Magic!')


@app.route('/upload_files', methods=['POST'])
def upload_files():
    file = request.files
    file_part = file['data_file']

    file_upload_service_obj = file_upload_service.File_Upload_Service()
    file_upload_service_obj.upload_file(file=file_part)

    return redirect(url_for('index'))


@app.route('/file_list', methods=['GET'])
def file_list():
    file_upload_service_obj = file_upload_service.File_Upload_Service()
    files = file_upload_service_obj.get_file_list()
    return jsonify(files) if len(files) is not 0 else jsonify(["No File Found!"])


@app.route('/clear_files', methods=['GET'])
def clear_files():
    file_upload_service.File_Upload_Service.move_all_files()

    return jsonify(["Uploaded images successfully removed!!"])


@app.route('/fetch_emotion', methods=['POST', 'GET'])
def process():
    try:
        res = prediction.Execute()
        return jsonify(res) if len(res) is not 0 else jsonify(dict(err="No File to Process!!"))
    except Exception as e:
        error_message = dumps({'Message': "Some Error on the Server! Inform the developer! "
                                          "Click Clear Images button and try again with a different pic."})
        abort(Response(error_message, 401))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
