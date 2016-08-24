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
import socket
import urllib2
import unicodedata

from docopt import docopt
from pprint import pprint
from tabulate import tabulate

CLIENT_ACCESS_TOKEN = 'Z1QtoNKtcX4F7ruB2QRaBnOK5n1SZNkOglv75XH7UvOSREikN6FceDaZoQLZBeyq'

def song_find(search_query_string):
    """Find song lyrics based on search query.

    Parameters
    ----------
    search_query_string: str
    The string to use as a search query.

    Prints
    -------
    result: json_obj
    Result for the parsed response.
    """
    querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_query_string) + "&page=1"
    request = urllib2.Request(querystring)
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
    body = json_obj["response"]["hits"]

    # Instantiate list to hold all the lyrics search results.
    lyrics = []
   
    for result in body:
        # Append each lyric property to a list and append that
        # list to the lyrics list.
        lyric = []
        lyric.append(result["result"]["id"])
        lyric.append(result["result"]["title"])
        lyric.append(result["result"]["primary_artist"]["name"])
        lyrics.append(lyric)
    # Tabulate our output...
    print tabulate(lyrics, ["ID", "Title", "Artist",], tablefmt="fancy_grid")

def song_view(song_id):
    """View song lyrics based on the song ID provided.

    Parameters
    ----------
    song_id: int
    The integer to use to get the song lyrics.

    Prints
    -------
    referent: json_obj
    Result for the parsed response.
    """
    querystring = "http://api.genius.com/referents?song_id={0}".format(song_id)
    request = urllib2.Request(querystring)
    request.add_header("Authorization", "Bearer " + CLIENT_ACCESS_TOKEN)
    request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")

    try:
        response = urllib2.urlopen(request, timeout=4)
        raw = response.read()
    except socket.timeout:
        pprint("Sorry, timed out. Try again later")
    
    json_obj = json.loads(raw)
    
    # All anotatable contents on Genius are called referents
    for referent in json_obj['response']['referents']:
        print referent['fragment'].rstrip()

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
