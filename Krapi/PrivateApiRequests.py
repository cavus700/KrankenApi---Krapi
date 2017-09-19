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


class Request_Specific_Orders(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to query order information.
    
    public request variables:
    trades:   whether or not to include trades in output (optional.  default = false)
    userref:  restrict results to given user reference id (optional)
    txid = comma delimited list of transaction ids to query info about (20 maximum)

    public response variables:
    orders_txid_dict : dict with order information and their txid's as keys.
                             See Get open orders/Get closed orders
                          
    """
    
    def __init__(self):
        super(Request_Specific_Orders, self).__init__()
        self.trades = 'false'
        self.userref  = None
        self.txid = []

        self.orders_txid_dict = {}
        
    def get_method(self):
        return "QueryOrders"

    def get_dict_data(self):
        transaction_ids = ''.join([id + ',' for id in self.txid])
        transaction_ids = transaction_ids[0:len(transaction_ids)-1]
        self.dict.update({'trades':self.trades, 'txid':transaction_ids})
        if self.userref is not None:
            self.dict.update({'userref':self.userref})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Specific_Orders, self).validate_response(response):
            return False
        else:
            self.orders_txid_dict = response['result']
            return True


class Request_Trade_History(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get trade history.
    
    public request variables:
    type:     type of trade  all = all types (default)
                             any position = any position (open or closed)
                             closed position = positions that have been closed
                             closing position = any trade closing all or part of a position
                             no position = non-positional trades
    trades:  whether or not to include trades related to position in output (optional.  default = false)
    start:   starting unix timestamp or trade tx id of results (optional.  exclusive)
    end:     ending unix timestamp or trade tx id of results (optional.  inclusive)
    offset:  result offset


    public response variables:
    trades_dict: array of trade info with txid as the key
    count: amount of available trades info matching criteria
                    
    Note: If the trade opened a position addtionial information is available (see official docu) and
    Unless otherwise stated, costs, fees, prices, and volumes are in the asset pair's scale, not the currency's scale.
    """
    
    def __init__(self):
        super(Request_Trade_History, self).__init__()
        self.type = 'any position'
        self.trades = False
        self.start = None
        self.end = None
        self.offset = 0

        self.trades_dict = {}
        self.count = 0
        
    def get_method(self):
        return "TradesHistory"

    def get_dict_data(self):
        self.dict.update({'type':self.type, 'trades':str(self.trades), 'ofs':str(self.offset)})
        if self.start is not None:
            self.dict.update({'start':str(self.start)})
        if self.end is not None:
            self.dict.update({'end':str(self.end)})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Trade_History, self).validate_response(response):
            return False
        else:
            self.trades_dict = response['result']['trades']
            self.count = response['result']['count']
            return True


class Request_Specific_Trades(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get information about specific trades.
    
    public request variables:
    txid:     comma delimited list of transaction ids to query info about (20 maximum)
    trades:   whether or not to include trades in output (optional.  default = false)

    public response variables:
    trades_txid_dict : dict with trade information and their txid's as keys.
                             (See Request_Trade_History)
                          
    """
    
    def __init__(self):
        super(Request_Specific_Trades, self).__init__()
        self.trades = 'false'
        self.txid = []

        self.trades_txid_dict = {}
        
    def get_method(self):
        return "QueryTrades"

    def get_dict_data(self):
        transaction_ids = ''.join([id + ',' for id in self.txid])
        transaction_ids = transaction_ids[0:len(transaction_ids)-1]
        self.dict.update({'txid':transaction_ids, 'trades':self.trades})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Specific_Trades, self).validate_response(response):
            return False
        else:
            self.trades_txid_dict = response['result']
            return True


class Request_Open_Positions(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get open positions and calculations.
    
    public request variables:
    txid:         comma delimited list of transaction ids to restrict output to
    calculations: whether or not to include profit/loss calculations (optional.  default = false)

    public response variables:
    position_txid_dict: dict with position information and their txid's as keys.
                            ordertxid = order responsible for execution of trade
                            pair = asset pair
                            time = unix timestamp of trade
                            type = type of order used to open position (buy/sell)
                            ordertype = order type used to open position
                            cost = opening cost of position (quote currency unless viqc set in oflags)
                            fee = opening fee of position (quote currency)
                            vol = position volume (base currency unless viqc set in oflags)
                            vol_closed = position volume closed (base currency unless viqc set in oflags)
                            margin = initial margin (quote currency)
                            value = current value of remaining position (if docalcs requested.  quote currency)
                            net = unrealized profit/loss of remaining position (if docalcs requested.  quote currency, quote currency scale)
                            misc = comma delimited list of miscellaneous info
                            oflags = comma delimited list of order flags
                            viqc = volume in quote currency
                          
    """
    
    def __init__(self):
        super(Request_Open_Positions, self).__init__()
        self.calculations = 'false'
        self.txid = []

        self.position_txid_dict = {}
        
    def get_method(self):
        return "OpenPositions"

    def get_dict_data(self):
        transaction_ids = ''.join([id + ',' for id in self.txid])
        transaction_ids = transaction_ids[0:len(transaction_ids)-1]
        self.dict.update({'txid':transaction_ids, 'docalcs':self.calculations})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Open_Positions, self).validate_response(response):
            return False
        else:
            self.trades_txid_dict = response['result']
            return True


class Request_Ledger_Info(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get ledger information.
    
    public request variables:
    aclass:     asset class (optional):
                    currency (default)
    asset_list: list of assets to restrict output to (optional.  default = all)
    type :      type of ledger to retrieve (optional):
                    all (default)
                    deposit
                    withdrawal
                    trade
                    margin
    start:      starting unix timestamp or ledger id of results (optional.  exclusive)
    end:        ending unix timestamp or ledger id of results (optional.  inclusive)
    offset:     result offset

    public response variables:
    amount:            number of ledger information
    ledger_info_dict:  dict with ledger information and their ledger id's as keys
                            <ledger_id> = ledger info
                                refid = reference id
                                time = unx timestamp of ledger
                                type = type of ledger entry
                                aclass = asset class
                                asset = asset
                                amount = transaction amount
                                fee = transaction fee
                                balance = resulting balance

    Note: Times given by ledger ids are more accurate than unix timestamps.                     
    """
    
    def __init__(self):
        super(Request_Ledger_Info, self).__init__()
        self.aclass = 'currency'
        self.asset_list = ['BCH', 'ZJPY', 'XICN', 'XLTC', 'EOS', 'ZKRW', 
                           'GNO', 'XZEC', 'ZGBP', 'XXMR', 'ZUSD', 'XXRP', 
                           'XXVN', 'ZEUR', 'XMLN', 'XXBT', 'DASH', 'KFEE', 
                           'XETH', 'XNMC', 'XETC', 'XXDG', 'USDT', 'XDAO', 
                           'ZCAD', 'XREP', 'XXLM']
        self.type = 'all'
        self.start = None
        self.end = None
        self.offset = 0

        self.ledger_info_dict = {}
        self.amount = 0
        
    def get_method(self):
        return "Ledgers"

    def get_dict_data(self):
        self.dict.update({'aclass':self.aclass})
        assets = ''.join([asset + ',' for asset in self.asset_list])
        assets = assets[0:len(assets)-1]
        self.dict.update({'asset':assets})
        self.dict.update({'type':str(self.type)})        
        if self.start is not None:
            self.dict.update({'start':self.start})
        if self.end is not None:
            self.dict.update({'end':self.end})
        self.dict.update({'ofs':str(self.offset)})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Ledger_Info, self).validate_response(response):
            return False
        else:
            self.amount = response['result']['count']
            self.ledger_info_dict = response['result']['ledger']
            return True


class Request_Specific_Ledgers(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get information about specific ledgers.
    
    public request variables:
    id: comma delimited list of transaction ids to query info about (20 maximum)

    public response variables:
    ledger_id_dict : dict with ledger information and their id's as keys.
                             (See Request_Ledger_Info)
                          
    """
    
    def __init__(self):
        super(Request_Specific_Ledgers, self).__init__()
        self.id = []

        self.ledger_id_dict = {}
        
    def get_method(self):
        return "QueryLedgers"

    def get_dict_data(self):
        ledger_ids = ''.join([id + ',' for id in self.id])
        ledger_ids = ledger_ids[0:len(ledger_ids)-1]
        self.dict.update({'id':transaction_ids})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Specific_Ledgers, self).validate_response(response):
            return False
        else:
            self.trades_txid_dict = response['result']
            return True


class Request_Trade_Volume(__Private_Request):
    """
    Overrides abstract methods from class __Private_Request.
    Creates a request to get information about specific ledgers.
    
    public request variables:
    asset_pair_list: comma delimited list of asset pairs to get fee info on (optional)
                        default all

    public response variables:
    currency: volume currency
    volume: current discount volume
    fees: dict of asset pairs and fee tier info
            fee = current fee in percent
            minfee = minimum fee for pair (if not fixed fee)
            maxfee = maximum fee for pair (if not fixed fee)
            nextfee = next tier's fee for pair (if not fixed fee.  nil if at lowest fee tier)
            nextvolume = volume level of next tier (if not fixed fee.  nil if at lowest fee tier)
            tiervolume = volume level of current tier (if not fixed fee.  nil if at lowest fee tier)
    fees_maker: array of asset pairs and maker fee tier info (if requested) for any pairs on maker/taker schedule
            fee = current fee in percent
            minfee = minimum fee for pair (if not fixed fee)
            maxfee = maximum fee for pair (if not fixed fee)
            nextfee = next tier's fee for pair (if not fixed fee.  nil if at lowest fee tier)
            nextvolume = volume level of next tier (if not fixed fee.  nil if at lowest fee tier)
            tiervolume = volume level of current tier (if not fixed fee.  nil if at lowest fee tier)
                          
    """
    
    def __init__(self):
        super(Request_Trade_Volume, self).__init__()
        self.asset_pair_list = ['XXBTZCAD', 'XXMRZUSD', 'XXBTZEUR', 'XETHXXBT', 'XXBTZGBP', 
                            'XETHZEUR', 'XXMRXXBT', 'XMLNXETH', 'XETHZJPY', 'XZECZEUR', 
                            'XREPXXBT', 'GNOXBT', 'XXBTZJPY', 'XXRPZUSD', 'XLTCZUSD', 
                            'XREPXETH', 'XXBTZGBP', 'XETHZUSD', 'EOSXBT', 'XETHZJPY', 
                            'XETHZCAD', 'XETCXXBT', 'XZECZUSD', 'XETHZGBP', 'BCHEUR', 
                            'XXDGXXBT', 'XXBTZEUR', 'XLTCZEUR', 'XETCXETH', 'XETHZGBP', 
                            'XREPZEUR', 'XXBTZCAD', 'XLTCXXBT', 'XXBTZJPY', 'XXMRZEUR', 
                            'XXBTZUSD', 'GNOETH', 'XETHZCAD', 'DASHXBT', 'XXLMXXBT', 
                            'XETCZEUR', 'XMLNXXBT', 'BCHUSD', 'XICNXETH', 'XETHXXBT', 
                            'XXRPXXBT', 'XETHZUSD', 'XXRPZEUR', 'EOSETH', 'DASHEUR', 
                            'XICNXXBT', 'XETCZUSD', 'XETHZEUR', 'XZECXXBT', 'DASHUSD', 
                            'XXBTZUSD', 'BCHXBT', 'USDTZUSD']

        self.currency = ''
        self.volume = 0
        self.fees = {}
        self.fees_maker = {}
        
    def get_method(self):
        return "TradeVolume"

    def get_dict_data(self):
        assets = ''.join([asset + ',' for asset in self.asset_pair_list])
        assets = assets[0:len(assets)-1]
        self.dict.update({'pair':assets})
        return self.dict

    def validate_response(self, response):
        if not super(Request_Trade_Volume, self).validate_response(response):
            return False
        else:
            self.currency = response['result']['currency']
            self.volume = response['result']['volume']
            self.fees = response['result']['fees']
            self.fees_maker = response['result']['fees_maker']
            return True