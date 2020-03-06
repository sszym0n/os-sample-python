from flask import Flask, request, Response, send_file
import os
import json
import binascii


application = Flask(__name__)


@application.route('/img', methods=['POST', 'GET'])
def saveImage():
    if request.method == 'POST':
        f = request.files['data']
        f.save('recv.jpg')
        application.logger.info("Saved file {}".format(f.filename))
        return Response(response='OK', status=200)
    elif request.method == 'GET':
        return send_file('recv.jpg', 'image/jpeg')


@application.route('/json', methods=['POST'])
def jsonSave():
    json_data = json.loads(request.get_json())

    index = json_data["index"]
    num_of_chunks = json_data["num_of_chunks"]
    buffer = binascii.a2b_base64(json_data["data"])
    fileMode = 'ab'
    if index == 0: fileMode = 'wb'

    try:
        with open('out.tmp', fileMode) as file:
            file.write(buffer)

        if index == num_of_chunks:
            os.rename('out.tmp', 'out.jpg')
    except OSError:
        return Response(response='OSError', status=500)

    return Response(response='OK', status=200)


@application.route("/")
def hello():
    return "File uploader"


if __name__ == "__main__":
    application.run()
