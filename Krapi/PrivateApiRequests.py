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

from Request import Request
from abc import ABCMeta, abstractmethod

class __Private_Request(Request):
    """
    Abstract class from which private requests should inherit.

    public methods:
    get_type(): returns that request is public 
    set_otp():  Sets the One-Time-Password for your private request

    abstract methods:
    get_method() - should return the request method as string
    get_dict_data() - should return POST data as dict
    """
    __metaclass__ = ABCMeta

    def get_type(self):
        return "private"
    
    def set_otp(self, otp):
        self.dict["otp"] = str(otp)

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def get_dict_data(self):
        pass

class Request_Balance(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get the account balance.
    
    public response variables:
    balance_dict: dictionary with assets as keys and balances as values    
    """
    
    def __init__(self):
        super(Request_Balance, self).__init__()
        self.balance_dict = {}
    
    def get_method(self):
        return "Balance"

    def get_dict_data(self):
        return self.dict

    def validate_response(self, response):
        if not super(Request_Balance, self).validate_response(response):
            return False
        else:
            self.balance_dict = response['result']
            return True


class Request_Trade_Balance(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get available trade balance.
    
    public request variables:
    asset_class: currency (default) 
    base_asset:  base asset used to determine balance (default = ZUSD)

    public response variables:
    asset_dict: dict with asset information and asset strings as keys
    """
    
    def __init__(self):
        super(Request_Trade_Balance, self).__init__()
        self.asset_class = 'currency'
        self.base_asset  = 'ZUSD'
        
    def get_method(self):
        return "TradeBalance"

    def get_dict_data(self):
        self.dict.update({'aclass':self.asset_class, 'asset':self.base_asset})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Trade_Balance, self).validate_response(response):
            return False
        else:
            self.balance_dict = response['result']
            return True