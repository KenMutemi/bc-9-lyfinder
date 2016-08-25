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
import cmd
import sys
import json
import socket
import urllib2
import contextlib

from docopt import docopt
from tabulate import tabulate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from pprint import pprint

from models import Lyric, Base
from authorize import Authorize

CLIENT_ACCESS_TOKEN = 'Z1QtoNKtcX4F7ruB2QRaBnOK5n1SZNkOglv75XH7UvOSREikN6FceDaZoQLZBeyq'
# Make a connection to our SQLite database
engine = create_engine('sqlite:///lyrics.db', echo=False)

# Creating our Session
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

def docopt_cmd(func):
    """ This is a decorator that simplifies the try/except block and passes
    the result of the docopt parsing to the called action.
    """
    pass

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

    authorize = Authorize(querystring)
    body = authorize.bot()
    # Instantiate list to hold all the lyrics search results.
    lyrics = []
   
    for result in body["response"]["hits"]:
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

    authorize = Authorize(querystring)
    json_obj = authorize.bot()
    
    # All anotatable contents on Genius are called referents
    for referent in json_obj['response']['referents']:
        print referent['fragment'].rstrip()

def song_save(song_id):
    """Save song lyrics based on the song ID provided.

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

    authorize = Authorize(querystring)
    json_obj = authorize.bot()
    # All anotatable contents on Genius are called referents
    referents = []
    for referent in json_obj['response']['referents']:
        referents.append(referent['fragment'].rstrip())
    lyric = Lyric(song_id=json_obj['response']['referents'][0]['annotatable']['id'], title=json_obj['response']['referents'][0]['annotatable']['title'], artist=json_obj['response']['referents'][0]['annotatable']['context'],  body=str(referents))
    session.add(lyric)
    session.commit()
    print "{0} by {1} has been saved.".format(json_obj['response']['referents'][0]['annotatable']['title'], json_obj['response']['referents'][0]['annotatable']['context'])

def song_clear():
    """Delete all the lyrics in local database."""
    try:
        num_rows_deleted = session.query(Lyric).delete()
        session.commit()
        print "{0} lyric(s) deleted!".format(num_rows_deleted)
    except:
        db.session.rollback()

class Interactive(cmd.Cmd):
    intro = 'Welcome to my Lyfinder!'\
            + ' (type help for a list of commands.)'

    promp = 'Lyfinder'
    file = None
    
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
