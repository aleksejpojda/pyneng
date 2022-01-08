# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""

import re
from sys import argv

def parse_sh_ip_int_br(status_file):
    regex = (
    r"(?P<intf>\S+) +"  #интерфейс
    r"(?P<ip>\d.+\d|unassigned) "    #ip
    r"+\S+ \S+ +"   #пропускаем
    r"(?P<status>up|administratively down|down) "     #статус
    r"+(?P<prot>up|down)"   #протокол
    )
    result = []
    with open(status_file) as f:
        output = f.read()
        m = re.finditer(regex, output)
        for match in m:
            result.append(match.groups())
    return result


#def parse_sh_ip_int_br(config_file):
#    regex = (
#    r"(?P<intf>\S+) +"  #интерфейс
#    r"(?P<ip>\d.+\d|unassigned) "    #ip
#    r"+\S+ \S+ +"   #пропускаем
#    r"(?P<status>up|(administratively )*down) "     #статус
#    r"+(?P<prot>up|down)"   #протокол
#    )
#    lists = []
#    with open(config_file) as f:
#        for line in f:
#            m = re.search(regex, line)
#            if m:
#                lists.append(tuple(m.group("intf", "ip", "status", "prot")))
#    return lists

if __name__ == "__main__":
    print(parse_sh_ip_int_br("sh_ip_int_br_2.txt"))