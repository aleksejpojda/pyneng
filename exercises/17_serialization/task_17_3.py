# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re

def parse_sh_cdp_neighbors(sh_cdp):
    result = {}
    port_local_dict = {}
    regex = r"(?P<host_rem>\S+) +(?P<port_local>\S+ \d+/\d+)." \
    r"+? (?P<port_rem>\S+ \d+/\d+)"
    host_local = re.search(r"(\S+)>", sh_cdp).group(1)
    for line in sh_cdp.split("\n"):
        match = re.search(regex, line)
        if match:
            port_local_dict[match.group("port_local")] = {}
            port_local_dict[match.group("port_local")][match.group("host_rem")] = match.group("port_rem")
    result[host_local] = port_local_dict
    return result





if __name__ == "__main__":
    with open("sh_cdp_n_r2.txt") as f:
        output = f.read()
    print(parse_sh_cdp_neighbors(output))