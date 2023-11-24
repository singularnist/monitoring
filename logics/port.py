from asyncio import Semaphore

import aiosnmp
from aiosnmp.exceptions import SnmpTimeoutError

from .save_db import Logics


class Port:

    def __init__(self) -> None:
        self.semaphore = Semaphore(50)
        self.logics =Logics()

    async def process_row(self, row:str) -> str:
        async with self.semaphore:
            async with aiosnmp.Snmp(host=row.IP_address, port=161, community="swenetro", timeout=4) as snmp:
                try:
                    p = 0
                    for resu in await snmp.get_bulk(".1.3.6.1.2.1.2.2.1.8", non_repeaters=0, max_repetitions=24):
                        if resu.value == 1:
                            p += 1
                    # print(f'Комутатор {row.name_sw} - портів {p}')
                    self.logics.save_port(row, p)
                except SnmpTimeoutError as e:
                    self.logics.save_down(row)
                    # print(e)
                except Exception as e:
                    print(e)



