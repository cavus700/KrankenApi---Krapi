#MIT License

#Copyright (c) [2017] [Robin Hubbig]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import httplib
import urllib
import hashlib
import base64
import hmac
import json
import time
from CredentialMgr import CredentialMgr
import RequestMgr
from Request import Request

class Kraken_Connector(object):
    """
    Handles connection with api.kraken.com
    Send and receives requests and responses.
    Supports the 'with' keyword

    public methods:
    query_request() - send a new request to api.kraken.com

    """

    def __init__(self):
        self.__url = 'https://api.kraken.com'
        self.__api_version = '0'
        self.__https_headers = { 'User-Agent': 'krapi/0.1.0 (+https://github.com/cavus700/KrankenApi---Krapi)' }
        self.__https_connection = httplib.HTTPSConnection('api.kraken.com', timeout = 20)
        self.__https_connection.connect()
            
    def __del__(self):
        self.__https_connection.close()

    def __enter__(self):
        self.__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def query_request(self, request, cred_mgr = None ):
        """
        Querys a request for api.kraken.com.

        Parameters:
        :type request:   Request.Request
        :param request:  Request class that provides all neccessary information

        :type cred_mgr:  CredentialMgr.CredentialMgr
        :param cred_mgr: CredentialMgr with loaded keys for private requests

        :return response as json

        :Exception - If cred_mgr not set for private request or request type is unknown

        """

        url_suff = '/' + self.__api_version + '/' + request.get_type() + '/' + request.get_method()

        if request.get_type() == 'public':
            return self.__send_request(url_suff, request.get_dict_data())

        elif request.get_type() == 'private':
            if not cred_mgr:
                raise Exception("Credential manager neccessary for private requests")

            headers, body = self.__compute_headers_and_nonce(url_suff, request.get_dict_data(), cred_mgr)
            return self.__send_request(url_suff, body, headers)
        else:
            raise Exception("Unknown request type: " + request.get_type() + ". Only public and private supported")


    def __send_request(self, url_suff, request = {}, headers = {}):
        """
        Actually send the request

        :type url_suff:  str
        :param url_suff: url suffix for request

        :type request:   dict
        :param request:  dictionary with POST data

        :type headers:  dict
        :param header:  additional headers for request

        :return response as json

        """

        url = self.__url + url_suff
        body = urllib.urlencode(request)
        headers.update(self.__https_headers)
        self.__https_connection.request("POST", url, body, headers)
        return json.loads(self.__https_connection.getresponse().read())

    def __compute_headers_and_nonce(self, url_suff, data, cred_mgr):
        """
        Computes the signature and additional headers for private request

        :type url_suff:  str
        :param url_suff: url suffix for request

        :type data:   dict
        :param data:  dictionary with POST data

        :type cred_mgr:  CredentialMgr.CredentialMgr
        :param cred_mgr: credential manager with loaded keys 

        :return  tuple with new header and POST data (header, data)

        """

        if not cred_mgr.get_credentials():
            raise Exception("No credentials set for private request")

        api_key, priv_key = cred_mgr.get_credentials()
    
        data['nonce'] = int(1000*time.time())
        postdata = urllib.urlencode(data)
        message = url_suff + hashlib.sha256(str(data['nonce']) + postdata).digest()
        signature = hmac.new(base64.b64decode(priv_key), message, hashlib.sha512)
        headers = {
            'API-Key': api_key,
            'API-Sign': base64.b64encode(signature.digest())
        }

        return (headers, data)