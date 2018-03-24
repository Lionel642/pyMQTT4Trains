import os
import sys
from sqlalchemy import create_engine

from inc import DB

# was 'sqlite:///pyMQTT4Trains.db'
engine = create_engine(DB.CONNSTRING)
DB.Base.metadata.create_all(engine)
