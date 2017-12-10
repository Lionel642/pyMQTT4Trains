import os
import sys
from sqlalchemy import create_engine

from lib import DB

engine = create_engine('sqlite:///pyMQTT4Trains.db')
DB.Base.metadata.create_all(engine)
