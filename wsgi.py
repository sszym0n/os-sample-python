from flask import Flask, request, Response, send_file
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
    json_data = json.loads(request.data)
    buffer = binascii.a2b_base64(json_data['image'])
    with open('recv.jpg', 'wb') as f:
        f.write(buffer)
    return Response(response='OK', status=200)


@application.route("/")
def hello():
    return "File uploader"


if __name__ == "__main__":
    application.run()
