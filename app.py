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

from docopt import docopt

def song_find(search_query_string):
    """Print the lyrics that match the search query."""
    print("song find, {0}".format(search_query_string))

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
