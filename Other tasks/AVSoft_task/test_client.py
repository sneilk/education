from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import json
import unittest

from sender import Sender


class TestNotebook(unittest.TestCase):

    def test_all_ok(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': ["load_folder/123.txt"],
                'server_path': ["save_folder/21.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        client = Sender(path)
        client.put()

    def test_wrong_adress(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': [],
                'server_path': []}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()

    def test_autentification_error(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'pass',
                'client_path': [],
                'server_path': []}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()

    def test_client_path_not_exist(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': ["load_folder/hello.txt"],
                'server_path': ["save_folder/123.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()

    def test_server_path_not_exist(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': ["load_folder/hello.txt"],
                'server_path': ["saving_folder/123.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()

    def test_json_source_not_exixts(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': ["load_folder/hello.txt"],
                'server_path': ["saving_folder/123.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender('path.json')
            client.put()

    def test_json_file_have_wrong_format(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'client_path': ["load_folder/hello.txt"],
                'server_path': ["saving_folder/123.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()

    def test_differ_len_of_client_server_paths(self):
        data = {
                'adress': '127.0.0.1',
                'login': 'user',
                'password': 'password',
                'client_path': ["load_folder/123.txt", "Hello.txt"],
                'server_path': ["save_folder/21.txt"]}

        path = 'config.json'
        with open(path, 'w') as f:
            f.write(json.dumps(data))

        with self.assertRaises(ValueError):
            client = Sender(path)
            client.put()
