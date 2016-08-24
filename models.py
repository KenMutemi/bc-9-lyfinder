from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class Lyric(Base):
    __tablename__ = 'lyrics'

    id = Column(Integer, primary_key=True)
    song_id = Column(String)
    title = Column(String)
    artist = Column(String)
    body = Column(String)
    
    def __repr__(self):
        return "%s by %s \n %s" % (self.title, self.artist, self.body)
