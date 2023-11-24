import asyncio
import time
from typing import List

from datebase import Switches, session_1

from .port import Port
from .up_time import Up_time


class Run:
    ''' Запуск '''
    
    def __init__(self) -> None:
        self.up_time = Up_time()

    async def process_data(self)->List:
        switches = session_1.query(Switches).all()
        tasks = [self.up_time.process_row(process_row) for process_row in switches]
        await asyncio.gather(*tasks)
        session_1.close()

    
    def run(self):

        loop = asyncio.get_event_loop()
        start_time = time.time()
        loop.run_until_complete(self.process_data())
        end_time = time.time()
        execution_time = end_time - start_time
        print("Час виконання: ", execution_time, "секунд")
    


