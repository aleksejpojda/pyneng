# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""

import re
from sys import argv

def get_ints_without_description(file):
    output = ""
    intf = []
    regex_des = r"interface (?P<intf>\S+)\n description"
    regex_intf = r"interface (?P<intf>\S+\d)"
    with open(file) as f:
        output = f.read()
        intf = re.findall(regex_intf, output)
        match = re.finditer(regex_des, output)
        if match:
            for m in match:
                intf.remove(m.group("intf"))
    return intf


#def get_ints_without_description(file):
#    regex_des = r"interface (?P<intf>\S+)\n description"
#    regex_intf = r"interface (?P<intf>\S+\d)"
#    intf = ""
#    output = ""
#    intf_list = []
#    with open(file) as f:
#        output = f.read()
#        for line in output.split("!"):
#            m = re.search(regex_intf, line)
#            if m:
#                m1 = re.search(regex_des, line)
#                if not m1:
#                    intf_list.append(m.group("intf"))
#    return intf_list

if __name__ == "__main__":
    print(get_ints_without_description("config_r1.txt"))