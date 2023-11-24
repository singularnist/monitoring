from datetime import datetime

from datebase import History, Switches, session_1


class Logics:
    def __init__(self) -> None:
        pass

    def save_down(self, row):
        ''' комутатор вимкнений '''
        current_datetime = datetime.now()
        time_ = current_datetime.strftime("%Y-%m-%d %H:%M")
        current_date = time_
        status= 0
        if row.stat != status:
            sw_entry = session_1.query(Switches).filter_by(ID=row.ID).first()
            if sw_entry:
                sw_entry.stat = status
            else:
                sw_entry = Switches(ID=row.ID, stat=status)
                session_1.add(sw_entry)

            monitoring_entry = session_1.query(History).filter_by(sw=row.name_sw, sw_off=None).order_by(History.ID.desc()).first()
            if monitoring_entry:
                monitoring_entry.sw_off = time_
                
            else:
                monitoring_entry = History(date=current_date, sw=row.name_sw, addres=row.address, off_power=time_, sw_off=time_)
                session_1.add(monitoring_entry)
            session_1.commit()
        
        elif row.stat == status:
            pass
    
    def save_reb(self, row):
        ''' комутатор перезавантажився'''
        current_datetime = datetime.now()
        time_ = current_datetime.strftime("%Y-%m-%d %H:%M")
        current_date = current_datetime.strftime("%Y-%m-%d")
        status= 1
        sw_entry = session_1.query(Switches).filter_by(ID=row.ID).first()

        if sw_entry:
            sw_entry.stat = status
        else:
            sw_entry = Switches(ID=row.ID, stat=status)
            session_1.add(sw_entry)

        monitoring_entry = session_1.query(History).filter(
            History.sw == row.name_sw,
            History.sw_on.is_(None)
        ).order_by(History.ID.desc()).first()

        if monitoring_entry:
            monitoring_entry.on_power = time_
            monitoring_entry.sw_on = time_
        else:
            monitoring_entry = History(
                date=time_,
                sw=row.name_sw,
                addres=row.address,
                off_power=time_,
                on_power=time_,
                sw_off=time_,
                sw_on=time_,
                ups_live=0,
                sw_down_time=0
            )
            session_1.add(monitoring_entry)
        session_1.commit()



    ''' комутатор включений '''
    def save_port(self, row, p):
        current_datetime = datetime.now()
        time_ = current_datetime.strftime("%Y-%m-%d %H:%M")
        current_date = time_
        status =1
        if row.stat != status:
            switch = session_1.query(Switches).filter_by(ID=row.ID).first()
            if switch:
                switch.stat = status
                session_1.commit()

                latest_monitoring = session_1.query(History).filter_by(sw=row.name_sw, sw_on=None).order_by(History.ID.desc()).first()
                if latest_monitoring:
                    latest_monitoring.on_power = time_
                    latest_monitoring.sw_on = time_
                    session_1.commit()
                else:
                    new_monitoring = History(date=current_date, sw=row.name_sw, addres=row.address, off_power=time_, on_power=time_, sw_off=time_, sw_on=time_)
                    session_1.add(new_monitoring)
                    session_1.commit()
        elif row.stat == status:
            if p != row.con:
                riz = row.con - p
                switch = session_1.query(Switches).filter_by(ID=row.ID).first()
                if switch:
                    switch.con = p
                    session_1.commit()
                    if p == 0:
                        new_monitoring = History(date=current_date, sw=row.name_sw, addres=row.address, off_power=time_)
                        session_1.add(new_monitoring)
                        session_1.commit()
                    elif row.con != 0:
                        if riz * 100 / row.con >= 17:
                            new_monitoring = History(date=current_date, sw=row.name_sw, addres=row.address, off_power=time_)
                            session_1.add(new_monitoring)
                            session_1.commit()
                        #### НИЖНІЙ IF НЕ ВИКОНУЄТЬСЯ, ДЕСЬ Я ПРОВТИКАВ
                        elif riz * 100 / row.con <= -10:
                            latest_monitoring = session_1.query(History).filter_by(sw=row.name_sw, on_power=None).order_by(History.ID.desc()).first()
                            if latest_monitoring:
                                latest_monitoring.on_power = time_
                                session_1.commit()
                            else:
                                new_monitoring = History(date=current_date, sw=row.name_sw, addres=row.address, off_power=time_, on_power=time_)
                                session_1.add(new_monitoring)
                                session_1.commit()
        else:
            print('Error 1')