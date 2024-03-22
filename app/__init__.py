from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .routes import *

app = Flask(__name__)
DB_URI = "sqlite:///fivetastic.db" 
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
app.config['DEBUG'] = True
