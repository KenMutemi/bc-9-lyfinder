"""
Lyfinder.

Usage:
  app.py song find <search_query_string>
  app.py song view <song_id>
  app.py song save <song_id>
  app.py song clear

Options:
  -h, --help    Show this message.
"""

import re
import json
import urllib2

from docopt import docopt

def load_credentials():
    lines = [line.rstrip('\n') for line in open('credentials.ini')]
    chars_to_strip = "\'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]

        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]

        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token

def song_find(search_query_string, client_access_token='Z1QtoNKtcX4F7ruB2QRaBnOK5n1SZNkOglv75XH7UvOSREikN6FceDaZoQLZBeyq'):
    """Print the lyrics that match the search query."""
    page = 1
    querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_query_string) + "&page=" + str(page)
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)
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
    body = json_obj["response"]["hits"]
   
    for result in body:
        print(result["result"]["id"])

def song_view(song_id):
    """Print the lyrics of the song ID provided."""
    print("song view, {0}".format(song_id))

def song_save(song_id):
    """Save the lyrics of the song ID provided."""
    print("song save, {0}".format(song_id))

def song_clear():
    """Delete all the lyrics in local database."""
    print("Clear all songs!")

if __name__ == '__main__':
    arguments = docopt(__doc__)

    # If an argument is was passed, execute its logic
    if arguments['song'] and arguments['find']:
        song_find(arguments['<search_query_string>'])

    elif arguments['song'] and arguments['view']:
        song_view(arguments['<song_id>'])

    elif arguments['song'] and arguments['save']:
        song_save(arguments['<song_id>'])

    elif arguments['song'] and arguments['clear']:
        song_clear()
