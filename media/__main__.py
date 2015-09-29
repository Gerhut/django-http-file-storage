from flask import *
import os.path, uuid, io, urlparse

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MEDIA_ROOT'] = os.path.join(os.path.dirname(__file__), 'files')
app.config['MEDIA_URL'] = 'http://127.0.0.1:5000/'

@app.route("/<filename>")
def get(filename):
    return send_from_directory(app.config['MEDIA_ROOT'], filename)

@app.route("/<filename>", methods=['PUT'])
def put(filename):
    extension = os.path.splitext(filename)[1]
    filename = uuid.uuid4().hex + extension
    pathname = os.path.join(app.config['MEDIA_ROOT'], filename)
    with io.open(pathname, 'wb') as file:
        for chunk in request.stream:
            file.write(chunk)
    url_root = app.config.get('MEDIA_URL', request.url_root)
    location = urlparse.urljoin(url_root, filename)
    response = make_response('', 201, { "Location": location })
    del response.headers['Content-Type']
    return response

if __name__ == '__main__':
    app.run()
