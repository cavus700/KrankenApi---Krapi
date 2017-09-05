import sys
from CredentialMgr import CredentialMgr
from RequestMgr import Request_Mgr
from PublicApiRequests import * 
from PrivateApiRequests import *
import json
import KrakenConnector

def main(argv):
    #public_request()
    private_request()
    return

##################################################################
### Short example of how to use the api for a private request ####
##################################################################

def private_request():
    cre_mgr = CredentialMgr()
    try:
        if not cre_mgr.encrypt_keys(in_file="KrakenKey.txt", pwd="Test"):
            print "Encryption failed"
            return
    except Exception as e:
        print e
        return

    if cre_mgr.load_credentials(tbk_file="KrakenKey.tbk", pwd="Test"):
        print 'Loading keys successfull'
    else:
        print 'Loading keys failed'
        return

    req_mgr = Request_Mgr(3)
    req_mgr.set_keys(cre_mgr)
    req = Request_Balance()

    if not req_mgr.send_request(req):
        if req.has_errors:
            print req.errors
    else:
        print req.raw_response


#################################################################
### Short example of how to use the api for a public request ####
#################################################################

def public_request():    
    req_mgr = Request_Mgr(3)
    req = Request_Time()
    if not req_mgr.send_request(req):
       if req.has_errors:
            print req.errors
    else:
        print req.raw_response

if __name__ == "__main__":
    main(sys.argv)