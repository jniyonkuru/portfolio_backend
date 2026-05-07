#resource form this party packages

from sqlalchemy.orm import sessionmaker,Session

#  resource from local packages
from app.db.db_config import engine

LocalSession=sessionmaker(bind=engine)


