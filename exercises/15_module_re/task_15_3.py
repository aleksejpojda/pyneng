# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re
from sys import argv

def convert_ios_nat_to_asa(input_file, output_file):
    file_out = ""
    regex = r"ip nat \D+ (?P<ip>\d.+\d) +(?P<port>\d+) interface (?P<intf>\S+) (?P<in_port>\d+)"
    with open(input_file) as f:
        output = f.read()
        match = re.finditer(regex, output)
        if match:
            for m in match:
                file_out += (
                    "object network LOCAL_{}\n".format(m.group("ip")) +\
                    " host {}\n".format(m.group("ip")) +\
                    " nat (inside,outside) static interface service tcp {} {}\n"\
                    .format(m.group("port"), m.group("in_port"))
                    )
    with open(output_file, "w") as f:
        f.write(file_out)
    return None



#def convert_ios_nat_to_asa(input_file, output_file):
#    file_out = ""
#    regex = r"ip nat \D+ (?P<ip>\d.+\d) +(?P<port>\d+) interface (?P<intf>\S+) (?P<in_port>\d+)"
#    with open(input_file) as f:
#        for line in f:
#            m = re.search(regex, line)
#            if m:
#                file_out += "object network LOCAL_" + m.group("ip")+"\n"
#                file_out += " host "+m.group("ip")+"\n"
#                file_out += (
#                " nat (inside,outside) static interface service tcp " + m.group("port") + \
#                " " + m.group("in_port") + "\n"
#                )
#    with open(output_file, "w") as f:
#        f.write(file_out)
#    return None

if __name__ == "__main__":
    print(convert_ios_nat_to_asa("cisco_nat_config.txt", "cisco_asa_nat_config.txt"))