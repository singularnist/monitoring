import datetime
import os
import time
from datetime import datetime
from threading import Thread

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datebase import History


class Corect:

    def __init__(self) -> None:
        pass

    def ups(self):
        load_dotenv()
        db_url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('TZ_DB')}"
        engine = create_engine(db_url)

        Session = sessionmaker(bind=engine)
        while True:
            session_1 = Session()
            query = session_1.query(History).filter(
                History.off_power.isnot(None),
                History.sw_off.isnot(None),
                History.ups_live.is_(None)
            ).order_by(History.ID.desc()).limit(1)

            record = query.first()
            if record is not None:
                time_of_power =  datetime.strptime(record.off_power, '%Y-%m-%d %H:%M')
                time_sw_off =  datetime.strptime(record.sw_off, '%Y-%m-%d %H:%M')
                riz_time = time_sw_off - time_of_power
                ups_live = int(riz_time.total_seconds() / 60)

                record.ups_live = ups_live
                session_1.commit()
                time.sleep(3)
            else:
                session_1.close()
                time.sleep(3)


    def down(self):
        load_dotenv()
        db_url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('TZ_DB')}"
        engine = create_engine(db_url)

        Session = sessionmaker(bind=engine)
        while True:
            session_1 = Session()
            query = session_1.query(History).filter(
                History.sw_off.isnot(None),
                History.sw_on.isnot(None),
                History.sw_down_time.is_(None)
            ).order_by(History.ID.desc()).limit(1)

            record = query.first()
            if record is not None:
                time_sw_off =  datetime.strptime(record.sw_off, '%Y-%m-%d %H:%M')
                time_sw_on = datetime.strptime(record.sw_on, '%Y-%m-%d %H:%M')
                riz_time = time_sw_on - time_sw_off
                sw_down = int(riz_time.total_seconds() / 60)

                record.sw_down_time = sw_down
                session_1.commit()
                session_1.close()
                time.sleep(3)
            else:
                session_1.close()
                time.sleep(3)


    def delete(self):
        load_dotenv()
        db_url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('TZ_DB')}"
        engine = create_engine(db_url)

        Session = sessionmaker(bind=engine)
        while True:
            session_1 = Session()
            query = session_1.query(History).filter(
                History.off_power.isnot(None),
                History.on_power.isnot(None),
                History.sw_off.is_(None),
                History.sw_on.is_(None)
            )

            query.delete()
            session_1.commit()
            session_1.close()
            time.sleep(5)


    def del_blef(self):
        load_dotenv()
        db_url = f"mysql+pymysql://{os.getenv('USER_DB')}:{os.getenv('PASS_DB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('TZ_DB')}"
        engine = create_engine(db_url)

        Session = sessionmaker(bind=engine)
        while True:
            session_1 = Session()
            current_time = datetime.now()
            
            query = session_1.query(History).filter(
                History.off_power.isnot(None),
                History.on_power.is_(None),
                History.sw_off.is_(None),
                History.sw_on.is_(None)
            )

            for record in query.all():
                time_off_power = datetime.strptime(record.off_power, '%Y-%m-%d %H:%M')
                time_difference = current_time - time_off_power
                minutes_difference = int(time_difference.total_seconds() / 60)

                if minutes_difference > 480:
                    session_1.delete(record)

            session_1.commit()
            session_1.close()
            time.sleep(5)


    def start(self):
        ups_time = Thread(target=self.ups)
        down_time = Thread(target=self.down)
        del_sql  = Thread(target=self.delete)
        del_blef_ = Thread(target=self.del_blef)
        ups_time.start()
        down_time.start()
        del_sql.start()
        del_blef_.start()

