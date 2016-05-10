import json

import requests
from python import deserialize_results, serialize_python_function

SETTINGS_FILE = 'settings.json'
VERSION_NUMBER = 0.1


class Server(object):

    def __init__(self):

        settings = json.load(open(SETTINGS_FILE, 'r'))

        # required settings
        try:
            self.url = settings['server_url']
        except KeyError:
            raise KeyError('Could not load server url from settings file')

        self.serializer = serialize_python_function

    def python(self, _function, *args):
        """Call a python function remotely
        Args:
            _function (str): function to call
            args (tuple): arguments to be passed to the given function

        Returns function result
        """

        return self._remote_call('python', _function, args)

    def r(self, _function, *args):
        """Call an R function remotely"""

        return self._remote_call('r', _function, args)

    def _remote_call(self, language, _function, args):
        """Execute remote call"""
        data = {
            'version': VERSION_NUMBER,
            'language': language
        }
        function_data = self.serializer(_function, args)
        data.update(function_data)
        response = requests.post(self.url, data=json.dumps(data))
        return deserialize_results(response.text)
