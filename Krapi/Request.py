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

from abc import ABCMeta, abstractmethod

class Request:
    """
    Initiates a new request.
    """
    
    __metaclass__ = ABCMeta

    def __init__(self):
        self.raw_response = {}
        self.has_errors = False
        self.errors = []
        self.dict = {}

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def get_dict_data(self):
        pass

    def validate_response(self, response):
        if 'error' in response:
            if response['error']:
                self.has_errors = True
                self.errors = response['error']
                return False
        self.raw_response = response
        return True