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
    balance_info_dict : dict with trade balance information.
                            eb = equivalent balance (combined balance of all currencies)
                            tb = trade balance (combined balance of all equity currencies)
                            m = margin amount of open positions
                            n = unrealized net profit/loss of open positions
                            c = cost basis of open positions
                            v = current floating valuation of open positions
                            e = equity = trade balance + unrealized net profit/loss
                            mf = free margin = equity - initial margin (maximum margin available to open new positions)
                            ml = margin level = (equity / initial margin) * 100

    """
    
    def __init__(self):
        super(Request_Trade_Balance, self).__init__()
        self.asset_class = 'currency'
        self.base_asset  = 'ZUSD'

        self.balance_info_dict = {}
        
    def get_method(self):
        return "TradeBalance"

    def get_dict_data(self):
        self.dict.update({'aclass':self.asset_class, 'asset':self.base_asset})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Trade_Balance, self).validate_response(response):
            return False
        else:
            self.balance_info_dict = response['result']
            return True

class Request_Open_Orders(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get information about open orders.
    
    public request variables:
    trades:   whether or not to include trades in output (optional.  default = false)
    userref:  restrict results to given user reference id (optional)

    public response variables:
    open_orders_dict : dict with open orders and their txid's as keys.
                            refid = Referral order transaction id that created this order
                            userref = user reference id
                            status = status of order:
                                pending = order pending book entry
                                open = open order
                                closed = closed order
                                canceled = order canceled
                                expired = order expired
                            opentm = unix timestamp of when order was placed
                            starttm = unix timestamp of order start time (or 0 if not set)
                            expiretm = unix timestamp of order end time (or 0 if not set)
                            descr = order description info
                                pair = asset pair
                                type = type of order (buy/sell)
                                ordertype = order type (See Add standard order)
                                price = primary price
                                price2 = secondary price
                                leverage = amount of leverage
                                order = order description
                                close = conditional close order description (if conditional close set)
                            vol = volume of order (base currency unless viqc set in oflags)
                            vol_exec = volume executed (base currency unless viqc set in oflags)
                            cost = total cost (quote currency unless unless viqc set in oflags)
                            fee = total fee (quote currency)
                            price = average price (quote currency unless viqc set in oflags)
                            stopprice = stop price (quote currency, for trailing stops)
                            limitprice = triggered limit price (quote currency, when limit based order type triggered)
                            misc = comma delimited list of miscellaneous info
                                stopped = triggered by stop price
                                touched = triggered by touch price
                                liquidated = liquidation
                                partial = partial fill
                            oflags = comma delimited list of order flags
                                viqc = volume in quote currency
                                fcib = prefer fee in base currency (default if selling)
                                fciq = prefer fee in quote currency (default if buying)
                                nompp = no market price protection
                            trades = array of trade ids related to order (if trades info requested and data available)

    Note: Unless otherwise stated, costs, fees, prices, and volumes are in the asset pair's scale, not the currency's scale. 
          For example, if the asset pair uses a lot size that has a scale of 8, the volume will use a scale of 8, 
          even if the currency it represents only has a scale of 2. Similarly, if the asset pair's pricing scale is 5, 
          the scale will remain as 5, even if the underlying currency has a scale of 8.
    """
    
    def __init__(self):
        super(Request_Open_Orders, self).__init__()
        self.trades = 'false'
        self.userref  = None

        self.open_orders_dict = {}
        
    def get_method(self):
        return "OpenOrders"

    def get_dict_data(self):
        self.dict.update({'trades':self.trades})
        if self.userref is not None:
            self.dict.update({'userref':self.userref})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Open_Orders, self).validate_response(response):
            return False
        else:
            self.open_orders_dict = response['result']['open']
            return True

class Request_Closed_Orders(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get information about closed orders.
    
    public request variables:
    trades:    whether or not to include trades in output (optional.  default = false)
    userref:   restrict results to given user reference id (optional)
    start:     starting unix timestamp or order tx id of results (optional.  exclusive)
    end:       ending unix timestamp or order tx id of results (optional.  inclusive)
    offset:    result offset
    closetime: which time to use (optional)
                open
                close
                both (default)
    
    public response variables:
    closed:  array of order info.  See Get open orders.  Additional fields:
        closetm - unix timestamp of when order was closed
        reason -  additional info on status (if any)
    count:    amount of available order info matching criteria

    Note: Times given by order tx ids are more accurate than unix timestamps. 
          If an order tx id is given for the time, the order's open time is used
    """
    
    def __init__(self):
        super(Request_Closed_Orders, self).__init__()
        self.trades = 'false'
        self.userref  = None
        self.start = None
        self.end = None
        self.offset = None
        self.close_time = 'both'

        self.closed_dict = {}
        self.count = 0
        
    def get_method(self):
        return "ClosedOrders"

    def get_dict_data(self):
        self.dict.update({'trades':self.trades})
        if self.userref is not None:
            self.dict.update({'userref':self.userref})
        if self.start is not None:
            self.dict.update({'start':str(self.start)})
        if self.end is not None:
            self.dict.update({'end':str(self.end)})
        if self.offset is not None:
            self.dict.update({'offset':str(self.offset)})
        self.dict.update({'closetime':self.close_time})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Closed_Orders, self).validate_response(response):
            return False
        else:
            self.closed_dict = response['result']['closed']
            self.count = response['result']['count']
            return True
