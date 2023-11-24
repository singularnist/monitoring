import time
from multiprocessing import Process

import schedule

from logics import Corect, Run


def job():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(current_time)
    run_instance = Run()
    run_instance.run()

def run():
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    monitoring = Process(target=run)
    corect= Corect()
    monitoring.start()
    time.sleep(5)
    corect.start()



    # schedule.every(5).minutes.do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # interval = 2 * 60
    # last_run_time = 0

    # while True:
    #     current_time = time.time()
    #     if current_time - last_run_time >= interval:
    #         job()
    #         last_run_time = current_time

    #     time.sleep(1)