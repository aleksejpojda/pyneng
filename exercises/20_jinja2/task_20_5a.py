# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

from pprint import pprint
from jinja2 import Environment, FileSystemLoader
import yaml
from netmiko import ConnectHandler
from task_18_1 import send_show_command
import re
from task_20_1 import generate_config
from task_18_2 import send_config_commands

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

def find_intf(src_device_params, dst_device_params):
    regex = r"Tunnel\d+"
    result_src = send_show_command(src_device_params, "sh ip int br | in Tunnel")
    result_dst = send_show_command(dst_device_params, "sh ip int br | in Tunnel")
    src = re.findall(regex, result_src)
    dst = re.findall(regex, result_dst)
    if src or dst:
        out = set(src) | set(dst)
        result = add_uniqe(out)
    else:
        result = "0"
    return result

def add_uniqe(set_1):
    name_intf = ",".join(re.findall(r"\D+", list(set_1)[0]))
    num_intf = int(",".join(re.findall(r"\d+", list(set_1)[0])))
    lenght = len(set_1)
    num_new=0
    while lenght == len(set_1):
        num_new +=1
        intf_new = name_intf+str(num_new)
        set_1.add(intf_new)
    return str(num_new)

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    vpn_data_dict["tun_num"] = find_intf(src_device_params, dst_device_params)
    vpn_src = generate_config(src_template, vpn_data_dict)
    vpn_dst = generate_config(dst_template, vpn_data_dict)
    result_src = send_config_commands(src_device_params, vpn_src.split("\n"))
    result_dst = send_config_commands(dst_device_params, vpn_dst.split("\n"))
    output_tuple = (result_src, result_dst)
    return output_tuple

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
#    print(add_uniqe(find_set_intf(devices[0], devices[1])))
#    print(find_intf(devices[0], devices[1]))
    print(configure_vpn(
        devices[0], devices[1], "templates/gre_ipsec_vpn_1.txt",
        "templates/gre_ipsec_vpn_2.txt", data
        ))