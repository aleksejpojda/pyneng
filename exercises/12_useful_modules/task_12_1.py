# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess



def ping_ip_addresses(ip_list):
    answ = ""
    reacheble_ip = []
    unreacheble_ip = []
    for ip in ip_list:
        answ = subprocess.run(["ping", "-c 3", "-i 0.3", ip])
        if answ.returncode == 0:
            reacheble_ip.append(ip)
        else:
            unreacheble_ip.append(ip)
    return reacheble_ip, unreacheble_ip

if __name__ == "__main__":
    addr = ["8.8.8.8", "1.1.1.1", "10.100.4.5"]
    print(ping_ip_addresses(addr))
