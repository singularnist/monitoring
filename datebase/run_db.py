import os

import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
# from db_model import Base
pymysql.install_as_MySQLdb()
load_dotenv()

db_url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('TZ_DB')}"


engine = create_engine(db_url, pool_size=50, max_overflow=50)

Session = sessionmaker(bind=engine)

session_1 = Session()

# articles = session_1.query(Switches).all()
# for article in articles:
#     print(article.name_sw)

# Base.metadata.create_all(engine)