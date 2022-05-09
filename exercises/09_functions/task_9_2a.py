# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо
  выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Пример итогового словаря, который должна возвращать функция (перевод строки
после каждого элемента сделан для удобства чтения):
{
    "FastEthernet0/1": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 10,20,30",
    ],
    "FastEthernet0/2": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 11,30",
    ],
    "FastEthernet0/4": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 17",
    ],
}

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from pprint import pprint


def generate_trunk_config(intf_vlan_mapping, trunk_template):
    res = {}
    for intf,vlan in intf_vlan_mapping.items():
        res_list = []
        for line in trunk_template:
            if "allowed vlan" in line:
                res_list.append(f"{line} {str(vlan[:])[1:-1].replace(' ', '')}")
            else: res_list.append(line)
        res[f"Interface {intf}"] = res_list
    return res




trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

def generate_trunk_config_1(intf_vlan_mapping, trunk_template):
    config = {}
    for intf, vlans in intf_vlan_mapping.items():
        cfg = []
        for  string in trunk_template:
            if string.endswith("vlan"):
                vlans = str(vlans[:])[1:-1]
                cfg.append(string + " " + vlans.replace(" ", ""))
            else:
                cfg.append(string)
        config[intf] = cfg
    return config

pprint(generate_trunk_config(trunk_config, trunk_mode_template))
