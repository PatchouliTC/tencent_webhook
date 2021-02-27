from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

#For alembic-Only import app.models.db.Base
from .models import *