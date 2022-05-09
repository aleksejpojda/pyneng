# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from sys import argv
from pprint import pprint


def get_int_vlan_map(config_filename):
    res_access = {}
    res_trunk = {}
    with open(config_filename) as f:
        file = f.read()
        intf = ""
        for line in file.split("\n"):
            if "interface" in line:
                intf = line.split()[-1]
            elif "access vlan" in line:
                res_access[intf] = int(line.split()[-1])
            elif "allowed" in line:
                res_trunk[intf] = [int(vl) for vl in line.split()[-1].split(",")]
    return res_access, res_trunk






def get_int_vlan_map_1(config_filename):

    output = ""
    cfg_section = ""
    #section = ""
    section_cfg_list = []
    intf = ""
    lines_trunk_vlan = ""
    lines_trunk_vlans = []
    trunk_vlans = []
    trunk_ports = {}
    access_ports = {}
    lines_access_vlans = []


    with open(config_filename) as f:
        output = f.read()
        cfg_section = output.replace(" "*9, "").split("!\n")
        for section in cfg_section:
    #         print(section.split("\n"))
            section_cfg_list = section.split("\n")
    #         print("-"*20)
            for line in section_cfg_list:

                if line.startswith("interface"):
                    intf=line.split()[1]
                if line.find("allowed vlan") != -1:
                    lines_trunk_vlan = line.split()[-1]
                    lines_trunk_vlans = lines_trunk_vlan.split(",")
                    trunk_vlans = []
                    for vlan in lines_trunk_vlans:
                        trunk_vlans.append(int(vlan))
                    trunk_ports[intf] = trunk_vlans
                if line.find("access vlan") != -1:
                    lines_access_vlans = int(line.split()[-1])
                    access_ports[intf] = lines_access_vlans
        return access_ports, trunk_ports


if __name__ == "__main__":
    pprint(get_int_vlan_map("config_sw1.txt"))
    pprint(get_int_vlan_map_1("config_sw1.txt"))