# bc-9-lyfinder
## Introduction
*  **`Lyfinder`** is a song lyrics console app.
*  It consists of the following features:
  *  Search for lyrics using any criteria
  *  View lyric selection by providing the id
  *  Save lyrics to the local database
  *  Delete all lyrics from the database
  *  Delete a particular lyric from the database
  *  Beautify lyrics to make them more readable and fun
  *  Lyrics Auto-scrolling features
*  Click [here](https://github.com/KenMutemi/bc-9-lyfinder) to access the app on Github

## Dependencies

*  This app's functionality depends on multiple Python packages including:
  *  **[Tabulate](https://pypi.python.org/pypi/tabulate)** - This package helps in the formatting of output in tabular format
  *  **[SQLAlchemy](http://www.sqlalchemy.org/)** - This is a python ORM that builds SQL statements that connect to the RDBMS
  *  **[Docopt](http://docopt.org/)** - This is a framework that is used to write command-line applications.
  *  **[Genius API](https://docs.genius.com/)** - The API used to fetch song lyrics.

## Installation and setup
*  Open a `terminal` and Navigate to a directory of choice.
*  Clone this repository on that directory.

    >git clone `https://github.com/KenMutemi/bc-9-lyfinder.git`

*  Navigate to the repo's folder on your computer
  *  `cd bc-9-lyfinder/`
*  Install the app's backend dependencies. Using a [virtual environment](http://virtualenv.readthedocs.org/en/latest/installation.html) is recommended.
  *  `pip install -r requirements.txt`
* Run the app
  *  `python app.py`
  *  Running the command above will open the app in interactive mode.

  ```
    (Lyfinder) ~$
  ```
