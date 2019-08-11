import socket
import json
from ftplib import FTP
import asyncio
import os


class Sender:
    """ Class to send files from client to server """

    def __init__(self, json_path):
        self._path = json_path
        self._adress = None
        self._login = None
        self._password = None
        self._server_path = None
        self._client_path = None
        self._ftp = None

    def parser(self):
        """ Parse data from config file """
        try:
            with open(self._path, 'r') as f:
                data = json.load(f)

            self._adress = data['adress']
            self._login = data['login']
            self._password = data['password']
            self._server_path = data['server_path']
            self._client_path = data['client_path']
        except:
            raise ValueError('Wrong path of config file')

        if len(self._server_path) != len(self._client_path):
            raise ValueError('Different length of paths')
        if (type(self._adress) is not str or
            type(self._login) is not str or
            type(self._password) is not str or
            type(self._server_path) is not list or
            type(self._client_path) is not list):
            raise ValueError("Wrong type of variables in json file")

    def put(self):
        """ Connect with server and call method to send files"""
        self.parser()
        try:
            self._ftp = FTP(
                host=self._adress, user=self._login, passwd=self._password)
        except:
            raise ValueError("Autentification error")
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.ftp_upload())
            loop.close()
        except:
            raise ValueError("Wrong client or server path")

    async def ftp_upload(self):
        """ Async output files from client to server"""
        for source, target in zip(self._client_path, self._server_path):
            ext = os.path.splitext(source)
            if ext in ['txt', 'html', 'htm']:
                with open(source, 'rb') as f:
                    self._ftp.storlines('STOR ' + target, f)
            else:
                with open(source, 'rb') as f:
                    self._ftp.storbinary(
                        'STOR ' + target, f, 1024)
            await asyncio.sleep(1.0)
