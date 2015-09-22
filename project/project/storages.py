from django.core.files.storage import Storage
from django.core.files import File

from django.utils.encoding import force_text, force_bytes

from django.conf import settings

from io import StringIO, BytesIO

import requests
from furl import furl

class HTTPStorageException(Exception):

    def __init__(self, message, cause=None):
        self.message = message
        self.cause = cause

    def __str__(self):
        result = self.message
        if self.cause is not None:
            result += ' ' + self.cause
        return result

class HTTPFile(File):

    def _parse_mode(self, mode):
        if not 'r' in mode:
            raise NotImplementedError()
        if 'w' in mode:
            raise NotImplementedError()
        if 'x' in mode:
            raise NotImplementedError()
        if 'a' in mode:
            raise NotImplementedError()
        if '+' in mode:
            raise NotImplementedError()

        self._binary = 'b' in mode

        if hasattr(self, _buffer):
            self._buffer.seek(0)
            buffer = self._buffer.read()
        else:
            buffer = None
            self._wrote = False

        if self._binary:
            self._buffer = BytesIO(force_bytes(buffer))
        else:
            self._buffer = StringIO(force_text(buffer))

    def __init__(self, name, mode, storage):

        self._parse_mode(mode)

        self._url = furl(storage.url).set(path=name).url
        self._storage = storage

        self.name = name
        self.mode = mode

        try:
            self.file = requests.get(self._url, stream=True)
            self.size = self.file.headers.get('content-length', None)
        except requests.exceptions.RequestException, e:
            raise HTTPStorageException('Request error', e)

    def open(self, mode=None):
        if mode is not None:
            self._parse_mode(mode)
        self.file.seek(0)

    def read(self, num_bytes=None):
        if num_bytes is None:
            content = self.file.read()
        else:
            content = self.file.read(num_bytes)

        if self._binary:
            content = force_bytes(content)
        else:
            content = force_text(content)

        return content

    def write(self, content):
        if self._binary:
            self._buffer.write(force_bytes(content))
        else:
            self._buffer.write(force_text(content))

        self._wrote = True

    def close(self):
        if self._wrote:
            self._buffer.seek(0)
            self._storage._save(self.name, self._buffer)
        self.file.close()
        self._buffer.close()

class HTTPStorage(Storage):

    def __init__(self, url=None):
        if url is None:
            url = settings.HTTP_STORAGE_URL
        self.url = url

    def _open(self, name, mode='rb'):
        return HTTPFile(name, mode, self)

    def _save(self, name, content):
        try:
            response = requests.post(self.url, data=content)

            if response.status_code != 201:
                raise requests.exceptions.HTTPError(
                    '%s %s' % (response.status_code, response.rason),
                    response=response)
        except requests.exceptions.RequestException, e:
            raise HTTPStorageException('Request error', e)

        try:
            location = response.headers['location']
        except KeyError:
            raise HTTPStorageException('No Location header in response.')

        try:
            path = furl(location).path
        except ValueError, e:
            raise HTTPStorageException('Location parsing error', e)

        return path.lstrip('/')
