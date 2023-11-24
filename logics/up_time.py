import asyncio
from asyncio import Semaphore

import aiosnmp
from aiosnmp.exceptions import SnmpTimeoutError

from .port import Port
from .save_db import Logics


class Up_time:
    ''' Клас перевірки Up Time '''

    def __init__(self) -> None:
        self.semaphore = Semaphore(50)
        self.port =Port()
        self.logics =Logics()

    async def process_row(self, row:str) -> str:
        async with self.semaphore:
            async with aiosnmp.Snmp(host=row.IP_address, port=161, community="swenetro", timeout=4) as snmp:
                try:
                    task = []
                    for res in await snmp.get(".1.3.6.1.2.1.1.3.0"):
                        reb = res.value / 60 /100 
                        if reb <=6:
                            self.logics.save_reb(row)
                            # print(f'Комутатор {row.name_sw} перезавантажився, {reb}')
                        else:
                            pass
                            # print(f'Все ок {row.name_sw} - {reb}')
                        task.append(self.port.process_row(row))
                    await asyncio.gather(*task)
                        
                except SnmpTimeoutError as e:
                    self.logics.save_down(row)
                    # print(f"SNMP Timeout Error for {row.IP_address}: {e} Комутатор {row.name_sw}")
                except Exception as e:
                    print(f"Помилковий статус {row.IP_address}: {e}, Комутатор {row.name_sw}")
    