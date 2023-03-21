from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

# visualization
from tabulate import tabulate
from termgraph import termgraph as tg

# database
from sqlalchemy import create_engine, Column,  Integer, DateTime, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class WorkInterval(Base):
    __tablename__ = 'work_intervals'
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        
    def __repr__(self):
        return "<WorkInterval(id='%s', start_time='%s', end_time='%s')>" % (self.id, self.start_time, self.end_time)
    
def setup_works_intervals(parser):
    parser.add_argument('-lt', '--log-time', choices=["in", "out"], required=False, help="log work time in database")
    parser.add_argument('-st', '--show-time', choices=["all-time", "today", "this-week", "this-month", "this-year"], required=False, help="show intervals for specified period as a number or specify -vt to select another visualization type")
    parser.add_argument('-vt', '--visualization-type', choices=["number", "table", "chart"], required=False, help="specift visualization type for -st")
    
    args = parser.parse_args()
    
    if args.log_time:
        log_time(args.log_time)
        
    if args.show_time:
        if not args.visualization_type or args.visualization_type == "number":
            print(format_seconds(get_total_time(get_work_intervals(args.show_time))))
        elif args.visualization_type == "table":
            visualize_work_interval_table(get_work_intervals(args.show_time))
        elif args.visualization_type == "chart":
            visualize_work_interval_chart(get_work_intervals(args.show_time))    
    

def log_time(logged: str):
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
        
def format_seconds(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

def get_total_time(intervals: List[WorkInterval]) -> int:
    total_time = 0
    for interval in intervals:
        if interval.end_time:
            total_time += (interval.end_time - interval.start_time).total_seconds()
        else:
            total_time += (datetime.now() - interval.start_time).total_seconds()

    return total_time
   
def get_work_intervals(period: str) -> List[WorkInterval]:    
    period_dict: Dict[str, Tuple[datetime, datetime]] = {
        'today': (datetime.today().date(), datetime.today().date() + timedelta(days=1)),
        'all-time': (datetime.min, datetime.max),
        'this-week': (datetime.today().date() - timedelta(days=datetime.today().weekday()), 
                      datetime.today().date() + timedelta(days=7-datetime.today().weekday())),
        'this-month': (datetime(datetime.today().year, datetime.today().month, 1),
                       datetime(datetime.today().year, datetime.today().month + 1, 1) - timedelta(days=1)),
        'this-year': (datetime(datetime.today().year, 1, 1),
                      datetime(datetime.today().year + 1, 1, 1) - timedelta(days=1))
    }
    
    engine: Engine = create_engine('sqlite:///work_intervals.sqlite')
    Base.metadata.create_all(bind=engine)

    Session: sessionmaker = sessionmaker(bind=engine)
    session: Session = Session()
    
    try:
        
        start_time: datetime
        end_time: datetime
        start_time, end_time = period_dict[period]
        Session: sessionmaker = sessionmaker(bind=engine)
        session: Session = Session()
        work_intervals: List[WorkInterval] = session.query(WorkInterval).filter(WorkInterval.start_time >= start_time, 
                                                                                WorkInterval.end_time <= end_time).all()
        return work_intervals
            
    except Exception as e:
        print("Error getting work intervals: " + str(e))
        return
    finally:
        session.close()
        engine.dispose()
        
def visualize_work_interval_table(intervals: List[WorkInterval]) -> None:
    """
    Visualizes work intervals as a table using the tabulate library.
    """
    
    table = [[interval.id, interval.start_time, interval.end_time] for interval in intervals]
    headers = ["ID", "Start Time", "End Time"]
    print(tabulate(table, headers=headers))
    
def visualize_work_interval_chart(intervals: List[WorkInterval]) -> None:
    """
    Visualizes work intervals as a bar graph using the termgraph library.
    """ 
    # Get the total duration of each day
    daily_durations: Dict[date, float] = {}
    for interval in intervals:
        date: date = interval.start_time.date()
        duration: float = (interval.end_time - interval.start_time).total_seconds() / 3600
        if date in daily_durations:
            daily_durations[date] += duration
        else:
            daily_durations[date] = duration

    values: List[List[float]] = []
    labels: List[str] = []
    for date in sorted(daily_durations.keys()):
        values.append([daily_durations[date]])
        labels.append(date.strftime("%Y-%m-%d"))
    
    # Set up the graph parameters and display the graph
    args: Dict[str, Any] = {'width': 80, 'suffix': ' hrs', 'no_labels': False, 'format': '{}'}
    tg.stacked_graph(labels, values, values, 1, args, [91])
    print(f"Total time: {format_seconds(get_total_time(intervals))}")