from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mssql+pyodbc://project:henhalaf4750@expressdns64")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

