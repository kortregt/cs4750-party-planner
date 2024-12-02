from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    future=True,
    isolation_level="AUTOCOMMIT"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
table_staff = Table('Staff', metadata, autoload_with=engine)
table_venue = Table('Venue', metadata, autoload_with=engine)
table_reservation = Table('Reservation', metadata, autoload_with=engine)