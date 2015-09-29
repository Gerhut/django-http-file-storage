from django.core.files.storage import Storage

from django.conf import settings

import os

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

class HTTPStorage(Storage):

    def __init__(self, remote=None):
        self.remote = str(remote) or settings.HTTP_STORAGE_REMOTE

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
