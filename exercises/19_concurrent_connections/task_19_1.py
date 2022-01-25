# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging


list_all_ip = ["192.168.100.1", "192.168.100.20", "192.168.100.3", "192.168.110.100"]

def ping_ip(ip_addresses):
    result = subprocess.run(["ping", "-c 3", ip_addresses], stdout=subprocess.DEVNULL)
    out = result.returncode
    return ip_addresses, out

def ping_ip_addresses(ip_list, limit=3):
    list_good = []
    list_bad = []
    with ThreadPoolExecutor(max_workers=limit) as ex:
        result = ex.map(ping_ip, ip_list)
        for ip, code in result:
            if code == 0:
                list_good.append(ip)
            else:
                list_bad.append(ip)
    list_good_bad = (list_good, list_bad)
    return list_good_bad

if __name__ == "__main__":
    print(ping_ip_addresses(list_all_ip))
