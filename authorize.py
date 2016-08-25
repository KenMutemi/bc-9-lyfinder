import json
import urllib2
CLIENT_ACCESS_TOKEN = 'Z1QtoNKtcX4F7ruB2QRaBnOK5n1SZNkOglv75XH7UvOSREikN6FceDaZoQLZBeyq'

class Authorize(object):
    """The __init__ method gets the querystring once the class is instantiated.
       The bot method acts as the user agent by providing headers and the access
             token.

    Args:
        querystring (str): A string containing the base url and the query 
                provided.

    """
    def __init__(self, querystring):
        self.querystring = querystring

    def bot(self):
        request = urllib2.Request(self.querystring)
        request.add_header("Authorization", "Bearer " + CLIENT_ACCESS_TOKEN)
        request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")
        while True:
            try:
                response = urllib2.urlopen(request, timeout=4)
                raw = response.read()
            except socket.timeout:
                print("Timeout")
                continue
            break

        json_obj = json.loads(raw)
        
        return json_obj
