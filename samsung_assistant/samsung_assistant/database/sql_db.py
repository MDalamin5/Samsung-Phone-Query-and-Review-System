# /database/sql_db.py
from sqlalchemy import create_engine, text
import pandas as pd

def get_sql_engine():
    """
    Creates and returns a SQLAlchemy engine for the MySQL database.
    """
    # Note: Ensure your user/password/db_name are correct.
    # It might be better to move these to the .env file as well.
    engine = create_engine('mysql+pymysql://root:@localhost/device_specs_db')
    return engine

def fetch_phone_data(engine, phone_name: str) -> str:
    """
    Fetches phone specifications from the database and returns them as a string.
    Returns an empty string if not found.
    """
    query = text("SELECT * FROM samsung_phone WHERE phone_name = :phone_name")
    
    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, connection, params={"phone_name": phone_name})
        
        if df.empty:
            return "" # Return empty string if no phone is found

        context_str = df.iloc[0].to_string()
        return context_str
    except Exception as e:
        print(f"Error fetching data from SQL DB: {e}")
        return ""

# Create a singleton instance
sql_engine = get_sql_engine()