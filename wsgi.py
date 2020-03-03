from flask import Flask, request, Response, send_file

application = Flask(__name__)


@app.route('/img', methods=['POST', 'GET'])
def saveImage():
    if request.method == 'POST':
        f = request.files['data']
        f.save('recv.jpg')
        application.logger.info("Saved file {}".format(f.filename))
        return Response(response='OK', status=200)
    elif request.method == 'GET':
        return send_file('recv.jpg', 'image/jpeg')


@app.route("/")
def hello():
    return "File uploader"


if __name__ == "__main__":
    application.run()
