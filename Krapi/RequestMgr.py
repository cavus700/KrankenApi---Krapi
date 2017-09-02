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

from threading import Timer, Lock
from CredentialMgr import CredentialMgr
from KrakenConnector import Kraken_Connector
from Request import Request

class Request_Mgr(object):
    """Handles all information needed for requests and sends them"""

    def __init__(self, tier, cred_mgr=None):
        """
        Supported tiers are 2, 3 and 4. 
        They are needed to determine the request limit.

        cred_mgr -- Credential manager for private requests

        :ValueError - If tier is not supported
        
        """

        if tier == 2:
            self._max_requests = 15
            self._request_reduce_interval = 3

        elif tier == 3:
            self._max_requests = 20
            self._request_reduce_interval = 2

        elif tier == 4:
            self._max_requests = 20
            self._request_reduce_interval = 1

        else:
            raise ValueError("Tier " + tier + " is not supported")

        self._current_requests = 0
        self._credentials_set = False
        self._credentials = None

        if cred_mgr:
            if isinstance(cred_mgr, CredentialMgr) and cred_mgr.get_credentials() != None:
                self._credentials = cred_mgr
                self._credentials_set = True

        self.__mutex = Lock()
        self.__timer = Timer(self._request_reduce_interval, self.__update_requests)
        self.__timer.daemon = True
        self.__timer.start()
        self.__connection = Kraken_Connector()

    def __del__(self):
        self.__timer.cancel()

    def set_keys(self, cred_mgr):
        """
        Sets the keys for private requests.

        :type cred_mgr: CredentialMgr.CredentialMgr
        :param requst: Credential manager with loaded keys

        :return - False - If cred_mgr is no instance of CredentialMgr or no credentials are loaded
                  True  - If setting of credentials was successfull 

        :ValueError - If request is not derived from Request.Request
        """

        if cred_mgr:
            if isinstance(cred_mgr, CredentialMgr) and cred_mgr.get_credentials() != None:
                self._credentials = cred_mgr
                self._credentials_set = True
                return True
        return False

    def send_request(self, request):
        """
        Send a request to api.kraken.com.

        :type request: derived class from Request.Request
        :param requst: public or private request for api.kraken.com

        :return - None - If send limit is excided or no key for private request is set. 
                  False - If request contains errors
                  True - If request was successfull

        :ValueError - If request is not derived from Request.Request
        """

        if not isinstance(request, Request):
            raise ValueError("Request parameter was no derived class of Request-Class")

        if request.get_type == 'private' and (not self._credentials_set or not self._credentials.get_credentials()) :
            return None

        # To avoid the 15 minute ban
        if self._current_requests == self._max_requests:
            return None

        with self.__mutex:
            self._current_requests += 1

        if request.get_type() == 'private':
            return request.validate_response(self.__connection.query_request(request, self._credentials))

        else:
            return request.validate_response(self.__connection.query_request(request))
                                             
    def __update_requests(self):
        """
        Update method to decrease request limit.
        Automatically called by a timer thread.

        """

        with self.__mutex:
            if self._current_requests > 0:
                self._current_requests -= 1
        self.__timer = Timer(self._request_reduce_interval, self.__update_requests)
        self.__timer.daemon = True
        self.__timer.start()

