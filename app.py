"""Lyfinder.

Usage:
  app.py 'song find' <search_query_string>
  app.py 'song view' <song_id>
  app.py 'song save' <song_id>
  app.py 'song clear'
  app.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
