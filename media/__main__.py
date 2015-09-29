from flask import *
import os, uuid, io, urlparse

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MEDIA_ROOT'] = os.path.join(os.path.dirname(__file__), 'files')
app.config['MEDIA_URL'] = 'http://127.0.0.1:5000/'

@app.route("/<path:pathname>")
def get(pathname):
    real_pathname = safe_join(app.config['MEDIA_ROOT'], pathname)

    if not os.path.exists(real_pathname):
        return abort(404)
    elif os.path.isdir(real_pathname):
        if pathname[-1] != '/':
            return redirect('/%s/' % (pathname,))
        else:
            return jsonify(entries=os.listdir(real_pathname))
    else:
        if pathname[-1] == '/':
            return redirect('/%s' % (pathname[:-1],))
        else:
            return send_file(real_pathname)

@app.route("/<path:pathname>", methods=['PUT'])
def put(pathname):
    try:
        real_pathname = safe_join(app.config['MEDIA_ROOT'], pathname)
    except:
        abort(403)

    real_directory = os.path.dirname(real_pathname)
    if not os.path.exists(real_directory):
        os.makedirs(real_directory)

    filename = uuid.uuid4().hex + os.path.splitext(pathname)[1]

    pathname = urlparse.urljoin(pathname, filename)
    real_pathname = os.path.join(real_directory, filename)

    with io.open(real_pathname, 'wb') as file:
        for chunk in request.stream:
            file.write(chunk)

    url_root = app.config.get('MEDIA_URL', request.url_root)
    location = urlparse.urljoin(url_root, pathname)
    response = make_response('', 201, { "Location": location })
    del response.headers['Content-Type']
    return response

if __name__ == '__main__':
    app.run()
