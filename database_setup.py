import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class JOBS(Base):
    __tablename__ = 'job'

    JobTile = Column(String(255), primary_key=True)
    CompanyName = Column(String(255), primary_key=False)
    FullTime = Column(Integer, nullable=False)
    Job=Column(Integer,nullable=False)
    Description=Column(String(10000),nullable=True)
    JobLink=Column(String(255),nullable=False)

engine = create_engine('mysql+pymysql://job:123@localhost:3306/JOB')


Base.metadata.create_all(engine)
