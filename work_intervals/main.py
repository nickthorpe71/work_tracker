from datetime import datetime
from sqlalchemy import create_engine, Column,  Integer,  DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class WorkInterval(Base):
    __tablename__ = 'work_intervals'
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        
    def __repr__(self):
        return "<WorkInterval(id='%s', start_time='%s', end_time='%s')>" % (self.id, self.start_time, self.end_time)

def log_time(logged):
    engine = create_engine('sqlite:///work_intervals.sqlite', echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    if logged == "in":
        try:
            existing_session_check = session.query(WorkInterval).filter(WorkInterval.end_time == None).first()
            if existing_session_check:
                print("You are already logged in")
                return
            interval = WorkInterval(datetime.now(), None)
            session.add(interval)
            session.commit()
            return
        except:
            print("Error logging in")
            return
            
    
    if logged == "out":
        try:
            interval = session.query(WorkInterval).filter(WorkInterval.end_time == None).first()
            if not interval:
                print("You are not logged in")
                return
            interval.end_time = datetime.now()
            session.commit()
            return
        except:
            print("Error logging out")
            return
    
    session.close()
    engine.dispose()
   
    
