from datetime import datetime, timedelta
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
    
def setup_works_intervals(parser):
    parser.add_argument('-lt', '--log-time', choices=["in", "out"], required=False, help="log work time in database")
    parser.add_argument('-st', '--show-time', choices=["all-time", "today", "this-week", "this-month", "this-year"], required=False, help="show work time from database")
    
    args = parser.parse_args()
    
    if args.log_time:
        log_time(args.log_time)
        
    if args.show_time:
        print(format_seconds(get_total_time(get_work_intervals(args.show_time))))

def log_time(logged):
    engine = create_engine('sqlite:///work_intervals.sqlite')
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
        except Exception as e:
            print("Error logging start time: " + str(e))
            return
            
    
    if logged == "out":
        try:
            interval = session.query(WorkInterval).filter(WorkInterval.end_time == None).first()
            if not interval:
                print("You are not logged in")
                return
            interval.end_time = datetime.now()
            session.commit()
            print(f"Total time: {format_seconds(get_total_time_today())}")
            return
        except Exception as e:
            print("Error logging end time: " + str(e))
            return
        
    
    session.close()
    engine.dispose()
    
def get_total_time_today():
    engine = create_engine('sqlite:///work_intervals.sqlite')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # get all intervals that have a start time today
        today = datetime.now().date()
        start = datetime(today.year, today.month, today.day, 0, 0, 0)
        end = start + timedelta(1)
        
        # get all intervals and filter out intervals that
        # don't have a start time between start and end
        intervals = session.query(WorkInterval).all()
        intervals = [interval for interval in intervals if interval.start_time >= start and interval.start_time < end]
        
        total_time = 0
        for interval in intervals:
            if interval.end_time:
                total_time += (interval.end_time - interval.start_time).total_seconds()
            else:
                total_time += (datetime.now() - interval.start_time).total_seconds()

        return total_time
    except Exception as e:
        print("Error getting work intervals: " + str(e))
        return
    finally:
        session.close()
        engine.dispose()
        
def format_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

def get_total_time(intervals):
    total_time = 0
    for interval in intervals:
        if interval.end_time:
            total_time += (interval.end_time - interval.start_time).total_seconds()
        else:
            total_time += (datetime.now() - interval.start_time).total_seconds()

    return total_time
    
   
def get_work_intervals(period):    
    period_dict = {
        'today': (datetime.today().date(), datetime.today().date() + timedelta(days=1)),
        'all-time': (datetime.min, datetime.max),
        'this-week': (datetime.today().date() - timedelta(days=datetime.today().weekday()), 
                      datetime.today().date() + timedelta(days=7-datetime.today().weekday())),
        'this-month': (datetime(datetime.today().year, datetime.today().month, 1),
                       datetime(datetime.today().year, datetime.today().month + 1, 1) - timedelta(days=1)),
        'this-year': (datetime(datetime.today().year, 1, 1),
                      datetime(datetime.today().year + 1, 1, 1) - timedelta(days=1))
    }
    
    engine = create_engine('sqlite:///work_intervals.sqlite')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        
        start_time, end_time = period_dict[period]
        Session = sessionmaker(bind=engine)
        session = Session()
        work_intervals = session.query(WorkInterval).filter(WorkInterval.start_time >= start_time, 
                                                            WorkInterval.end_time <= end_time).all()
        return work_intervals
            
    except Exception as e:
        print("Error getting work intervals: " + str(e))
        return
    finally:
        session.close()
        engine.dispose()

