from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()








def get_engine():
    db_name = os.getenv("db_name")
    db_user = os.getenv("db_user")
    db_host = os.getenv("db_host")
    db_password = os.getenv("db_password")

    url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}" 
    return create_engine(url)
