from flask import Flask, request, Response, send_file
import os
import json
import binascii


application = Flask(__name__)


@application.route('/img/<station>', methods=['POST', 'GET'])
def handle_image(station):
    if request.method == 'POST':
        f = request.files['data']
        f.save(station + '.jpg')
        application.logger.info("Data {}".format(request.headers))
        return Response(response='OK', status=200)
    elif request.method == 'GET':
        if os.path.exists(station + '.jpg'):
            return send_file(station + '.jpg', 'image/jpeg')
        else:
            return Response(response="No file for station", status=500)


@application.route('/json', methods=['POST'])
def handle_json():
    json_data = json.loads(request.get_json())

    index = json_data["index"]
    num_of_chunks = json_data["num_of_chunks"]
    file_name = json_data["station_name"] + ".jpg"
    temp_file = json_data["station_name"] + ".tmp"
    buffer = binascii.a2b_base64(json_data["data"])
    file_mode = 'ab'
    if index == 0: file_mode = 'wb'

    try:
        with open(temp_file, file_mode) as file:
            file.write(buffer)

        if index == num_of_chunks:
            if os.path.exists(file_name):
                os.remove(file_name)
            os.rename(temp_file, file_name)

    except OSError as e:
        application.logger.info(e)
        return Response(response='OSError', status=500)

    return Response(response='OK', status=200)


@application.route("/")
def hello():
    return "File uploader"


if __name__ == "__main__":
    application.run()
