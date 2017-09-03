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

class __Public_Request(Request):
    """
    Abstract class from which public requests should inherit

    public methods:
    get_type(): returns that request is public 

    abstract methods:
    get_method() - should return the request method as string
    get_dict_data() - should return POST data as dict
    """
    __metaclass__ = ABCMeta

    def get_type(self):
        return "public"
    
    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def get_dict_data(self):
        pass

class Request_Time(__Public_Request):
    """
    Overrides abstract methods from class __Public_Request
    Creates a request to get the server time.
    
    public response variables:
    unixtime: contains the server time after successfull request
    rfc1123:  contains the server time  in rfc1123 standard after successfull request
    """
    
    def __init__(self):
        super(Request_Time, self).__init__()
        self.unixtime = None
        self.rfc1123 = None

    def get_method(self):
        return "Time"

    def get_dict_data(self):
        return self.dict

    def validate_response(self, response):
        if not super(Request_Time, self).validate_response(response):
            return False
        else:
            self.unixtime = response['result']['unixtime']
            self.rfc1123 = response['result']['rfc1123']
            return True


class Request_Assets(__Public_Request):
    """
    Overrides abstract methods from class __Public_Request
    Creates a request to get available assets
    
    public request variables:
    asset_list: list with assets as strings to enquire (default all) 

    public response variables:
    asset_dict: dict with asset information and asset strings as keys
    """
    
    def __init__(self):
        super(Request_Assets, self).__init__()
        self.asset_list = ['BCH', 'ZJPY', 'XICN', 'XLTC', 'EOS', 'ZKRW', 
                           'GNO', 'XZEC', 'ZGBP', 'XXMR', 'ZUSD', 'XXRP', 
                           'XXVN', 'ZEUR', 'XMLN', 'XXBT', 'DASH', 'KFEE', 
                           'XETH', 'XNMC', 'XETC', 'XXDG', 'USDT', 'XDAO', 
                           'ZCAD', 'XREP', 'XXLM']
        self.asset_dict = None

    def get_method(self):
        return "Assets"

    def get_dict_data(self):
        assets = ''.join([asset + ',' for asset in self.asset_list])
        assets = assets[0:len(assets)-1]
        self.dict.update({'info':'info', 'aclass':'currency', 'asset':assets})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Assets, self).validate_response(response):
            return False
        else:
            self.asset_dict = response['result']
            return True


class Request_Tradable_Asset_Pairs(__Public_Request):
    """
    Overrides abstract methods from class __Public_Request
    Creates a request to get information for asset pairs
    
    public request variables:
    asset_pair_list: list with asset pairs as strings to enquire (default all) 
    info:            Options: 'info'     - all info (default)
                             'leverage' - leverage info
                             'fees'     - fees schedule
                             'margin'   - margin info
    public response variables:
    asset_pairs_dict: dict with asse pair information and asset pair strings as keys
    """
    
    def __init__(self):
        super(Request_Tradable_Asset_Pairs, self).__init__()
        self.info = 'info'
        self.asset_pair_list = ['XXBTZCAD', 'XXMRZUSD', 'XXBTZEUR.d', 'XETHXXBT', 'XXBTZGBP.d', 
                            'XETHZEUR', 'XXMRXXBT', 'XMLNXETH', 'XETHZJPY', 'XZECZEUR', 
                            'XREPXXBT', 'GNOXBT', 'XXBTZJPY.d', 'XXRPZUSD', 'XLTCZUSD', 
                            'XREPXETH', 'XXBTZGBP', 'XETHZUSD', 'EOSXBT', 'XETHZJPY.d', 
                            'XETHZCAD', 'XETCXXBT', 'XZECZUSD', 'XETHZGBP', 'BCHEUR', 
                            'XXDGXXBT', 'XXBTZEUR', 'XLTCZEUR', 'XETCXETH', 'XETHZGBP.d', 
                            'XREPZEUR', 'XXBTZCAD.d', 'XLTCXXBT', 'XXBTZJPY', 'XXMRZEUR', 
                            'XXBTZUSD.d', 'GNOETH', 'XETHZCAD.d', 'DASHXBT', 'XXLMXXBT', 
                            'XETCZEUR', 'XMLNXXBT', 'BCHUSD', 'XICNXETH', 'XETHXXBT.d', 
                            'XXRPXXBT', 'XETHZUSD.d', 'XXRPZEUR', 'EOSETH', 'DASHEUR', 
                            'XICNXXBT', 'XETCZUSD', 'XETHZEUR.d', 'XZECXXBT', 'DASHUSD', 
                            'XXBTZUSD', 'BCHXBT', 'USDTZUSD']
        self.asset_pairs_dict = None

    def get_method(self):
        return "AssetPairs"
    
    def get_dict_data(self):
        asset_pairs = ''.join([asset + ',' for asset in self.asset_pair_list])
        asset_pairs = asset_pairs[0:len(asset_pairs)-1]
        self.dict.update({'info':self.info, 'pair':asset_pairs})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Tradable_Asset_Pairs, self).validate_response(response):
            return False
        else:
            self.asset_pairs_dict = response['result']
            return True

