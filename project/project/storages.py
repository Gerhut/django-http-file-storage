from django.core.files.storage import Storage
from django.core.files import File

from django.utils.deconstruct import deconstructible
from django.conf import settings

import os, io

import requests
from furl import furl

class HTTPStorageException(Exception):

    def __init__(self, message, cause=None):
        self.message = message
        self.cause = cause

    def __str__(self):
        result = self.message
        if self.cause is not None:
            result += ' ' + str(self.cause)
        return result

class HTTPFile(File):

    def _open(self):
        response = requests.get(self.name)

        if 'b' in self.mode:
            self.file = io.BytesIO(response.content)
        else:
            self.file = io.StringIO(response.text)

    def __init__(self, name, mode='rb'):

        if 'w' in mode:
            raise NotImplementedError('Cannot write to HTTPFile.')
        if '+' in mode:
            raise NotImplementedError('Cannot append to HTTPFile.')

        self.name = name
        self.mode = mode
        self._open()

    def open(self, mode=None):
        if not self.closed and mode is None:
            self.seek(0)
        else:
            if mode is not None:
                self.mode = mode
            self._open()

    def write(self, content=''):
        raise NotImplementedError('Cannot write to HTTPFile.')

    def close(self):
        super(HTTPFile, self).close()

@deconstructible
class HTTPStorage(Storage):

    def __init__(self, remote=None):
        self.remote = str(remote) or settings.HTTP_STORAGE_REMOTE

    def _open(self, name, mode='rb'):
        return HTTPFile(name, mode)

    def _save(self, name, content):
        try:
            url = furl(self.remote).set(path=os.path.basename(name))
            response = requests.put(url, data=content)
            response.raise_for_status()
        except requests.exceptions.RequestException, e:
            raise HTTPStorageException('Request error', e)

        try:
            return response.headers['location']
        except KeyError:
            raise HTTPStorageException('No Location header in response.')

    def exists(self, name):
        return False

    def url(self, name):
        return name
