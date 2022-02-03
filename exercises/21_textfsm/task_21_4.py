# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from textfsm import clitable
import yaml
from netmiko import ConnectHandler
import netmiko
from task_21_3 import parse_command_dynamic


attrib =  {'Command': 'sh ip int br'}

def send_and_parse_show_command(device_dict, command, templates_path="templates", index="index"):
 #   out = []
    attrib['Command'] = command
    with ConnectHandler(**device_dict) as dev:
        dev.enable()
        output = dev.send_command(command)
    out = (parse_command_dynamic(output, attrib))
    return out

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        print(send_and_parse_show_command(dev, "sh version"))
        print(send_and_parse_show_command(dev, "sh ip int br"))