"""
Lyfinder.

Usage:
  app.py song find <search_query_string>

Options:
  -h, --help    Show this message.
"""

from docopt import docopt

def song_find(search_query_string):
    print("song find, {0}".format(search_query_string))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    # If an argument is was passed, execute its logic
    if arguments['song'] and arguments['find']:
        song_find(arguments['<search_query_string>'])
