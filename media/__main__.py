from flask import *
import os, uuid, urlparse

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MEDIA_ROOT'] = os.path.join(os.path.dirname(__file__), 'files')

@app.route("/<filename>")
def get(filename):
    return send_from_directory(app.config['MEDIA_ROOT'], filename)

@app.route("/<filename>", methods=['PUT'])
def put(filename):
    extension = os.path.splitext(filename)[1]
    filename = uuid.uuid4().hex + extension
    pathname = os.path.join(app.config['MEDIA_ROOT'], filename)
    file = open(pathname, 'w')
    file.write(request.stream.read())
    file.close()
    url_root = app.config.get('MEDIA_URL', request.url_root)
    location = urlparse.urljoin(url_root, filename)
    return '', 201, dict(Location=location)

if __name__ == '__main__':
    app.run()
