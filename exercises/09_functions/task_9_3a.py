# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
            elif "switchport mode access" in line:
                res_access[intf] = 1
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
                if line.find(" mode access") != -1:
                    lines_access_vlans = 1
                    access_ports[intf] = lines_access_vlans
        return access_ports, trunk_ports


#print(get_int_vlan_map(argv[1]))
if __name__ == "__main__":
   pprint(get_int_vlan_map("config_sw2.txt"))