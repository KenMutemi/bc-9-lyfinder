"""
Lyfinder.

Usage:
  app.py (-i | --interactive)
  app.py view song <song_id>
  app.py find song <search_query_string>
  app.py save song <song_id>
  app.py clear

Options:
  -h, --help    Show this message.
"""

import cmd
import os
import sys
import ast
import json
import socket
import random
import urllib2

from docopt import docopt, DocoptExit
from tabulate import tabulate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from models import Lyric, Base
from authorize import Authorize
from helpers import StringFormatter

# Make a connection to our SQLite database
engine = create_engine('sqlite:///lyrics.db', echo=False)

# Creating our Session
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class Lyfinder(cmd.Cmd):
    os.system('clear')
    intro = 'Welcome to Lyfinder!\n' \
            + ' (type help for a list of commands.)'

    prompt = '(Lyfinder) ~$ '
    file = None

    @docopt_cmd
    def do_find(self, search_query_string):
        """Usage: find song <search_query_string>"""
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
    
        querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_query_string['<search_query_string>']) + "&page=1"
    
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
        # Clear console
        os.system('clear')
        # Tabulate our output...
        print tabulate(lyrics, ["ID", "Title", "Artist",], tablefmt="fancy_grid")

    @docopt_cmd
    def do_view(self, song_id):
        """Usage: view song <song_id>"""
        """View song lyrics based on the song ID provided.
    
        Parameters
        ---------
        song_id: int
        The integer to use to get the song lyrics.
    
        Prints
        -------
        referent: json_obj
        Result for the parsed response.
        """
        # Colors to show in lyrics
        colors = [StringFormatter.BLUE, StringFormatter.CYAN, StringFormatter.DARKCYAN,
                StringFormatter.GREEN, StringFormatter.PURPLE, StringFormatter.RED]

        try:
    
            if session.query(Lyric.id).filter_by(song_id=song_id['<song_id>']).scalar() is not None:
                lyric = session.query(Lyric).filter_by(song_id=song_id['<song_id>']).first()
                body = ast.literal_eval(lyric.body)
                title = lyric.title
                artist = lyric.artist
        
                os.system('clear')

                print "{0}Showing {1} lyrics perforemed by {2} {3}".format(StringFormatter.BOLD, title, artist, StringFormatter.END)
        
                for referent in body:
                    print referent + random.choice(colors)
                print StringFormatter.END
                
            else:
                querystring = "http://api.genius.com/referents?song_id={0}".format(urllib2.quote(song_id['<song_id>']))
                authorize = Authorize(querystring)
                json_obj = authorize.bot()
        
                os.system('clear')
                
                # All anotatable contents on Genius are called referents
                print "{0}{1}Showing '{2}' lyrics performed by {3}{4}\n".format(StringFormatter.BOLD,
                        StringFormatter.UNDERLINE,
                        json_obj['response']['referents'][0]['annotatable']['title'],
                        json_obj['response']['referents'][0]['annotatable']['context'],
                        StringFormatter.END)
                for referent in json_obj['response']['referents']:
                    print referent['fragment'].rstrip() + random.choice(colors)
                print StringFormatter.END
        except (InvalidRequestError, urllib2.HTTPError):
            print "That was an invalid request! Please try again."

    @docopt_cmd
    def do_save(self, song_id):
        """Usage: save song <song_id>"""

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
    
        try:
            querystring = "http://api.genius.com/referents?song_id={0}".format(urllib2.quote(song_id['<song_id>']))
        
            authorize = Authorize(querystring)
            json_obj = authorize.bot()
            # All anotatable contents on Genius are called referents
            referents = []
            for referent in json_obj['response']['referents']:
                referents.append(referent['fragment'].rstrip())
            lyric = Lyric(song_id=json_obj['response']['referents'][0]['annotatable']['id'],
                    title=json_obj['response']['referents'][0]['annotatable']['title'],
                    artist=json_obj['response']['referents'][0]['annotatable']['context'],
                    body=str(referents))
            session.add(lyric)
            session.commit()

            os.system('clear')

            print song_id['<song_id>']

            print "{0} by {1} has been saved.".format(json_obj['response']['referents'][0]['annotatable']['title'],
                json_obj['response']['referents'][0]['annotatable']['context'])

        except (IntegrityError, InvalidRequestError):
            print "This song is already saved!"

    @docopt_cmd
    def do_clear(self, songs):
        """Usage: clear"""

        """Delete all the lyrics in local database."""
        try:
            num_rows_deleted = session.query(Lyric).delete()
            session.commit()
            os.system('clear')
            print "{0} lyric(s) deleted!".format(num_rows_deleted)
        except:
            db.session.rollback()

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Bye!')
        exit()
            
if __name__ == '__main__':
    arguments = docopt(__doc__, sys.argv[1:])
    if arguments['--interactive']:
        Lyfinder().cmdloop()
        print(arguments)

    # If an argument is was passed, execute its logic
    if arguments['song'] and arguments['find']:
        song_find(arguments['<search_query_string>'])

    elif arguments['song'] and arguments['view']:
        song_view(arguments['<song_id>'])

    elif arguments['song'] and arguments['save']:
        song_save(arguments['<song_id>'])

    elif arguments['song'] and arguments['clear']:
        song_clear()
