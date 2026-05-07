# resources from third part packages
from dotenv import load_dotenv
from sqlalchemy import create_engine
#resources form standard packages
import os
# resources from local packages
load_dotenv()

DATABASE_URL=os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=True)


