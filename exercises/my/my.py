# Write your code here :-)

from netmiko import ConnectHandler
import re, yaml
from concurrent.futures import ThreadPoolExecutor
from rich.table import Table
from rich.console import Console
from datetime import datetime
from sys import argv


time = datetime.now()
device1 = {'device_type': 'cisco_ios',
          "ip": "192.168.100.1",
          "username": "cisco",
          "password": "cisco",
          'secret': 'cisco'}

def send_show_command_to_devices(devices, limit=3):
    """ Подключение на несколько устройств одновременно.
    Принимает в себя список словарей с данными для подключения
    к нескольким устройствам. Лимит по умолчанию 3 устройства.
    Возвращает словарь с выводом устройства """
    out_dict = {}
    with ThreadPoolExecutor(max_workers=limit) as ex:
        result = ex.map(show_ip_int, devices)
    for res in result:
        out_dict.update(res)
    return out_dict

def show_ip_int(device):
    """ Отправка команды 'sh ip int br'.
    Принимает в себя словарь с данными для подключения
    Возвращает вывод устройства, строка
    Вызывает функцию 'parse_out' """
    with ConnectHandler(**device) as sw:
#        sw.enable()
        out = sw.send_command("sh ip int br")
        out_dict = parse_out(out, sw.host)
    return out_dict

def check_intf_type_status(list_dict, type_intf):
    """ Определяем статус портов.
    Принимает словарь со списком интерфейсов и состоянием,
    вторая переменная тип порта.
    Возвращает словарь для одного типа порта
    ключ: состояние порта, значение: список портов """
    list_intf_up = []
    list_intf_down = []
    list_intf_admin = []
    status_dict = {}
    key_status_list = ["up", "down", "admin"]
    status_dict = dict.fromkeys(key_status_list)
    for line in list_dict:
        intf = line['intf']
        if type_intf in intf and line['status'] == "up":
            list_intf_up.append(intf)
        elif type_intf in intf and line['status'] == "down":
            list_intf_down.append(intf)
        elif type_intf in intf and line['status'] == "administratively down":
            list_intf_admin.append(intf)
    status_dict["up"] = list_intf_up
    status_dict["down"] = list_intf_down
    status_dict["admin"] = list_intf_admin
    return status_dict

def parse_out(out_ip_int, dev_ip):
    """ Создаем словарь для устройства по типу портов и их состоянию
    Принимает строку с выводом от устройства и его адрес.
    Возвращает словарь: ключ - адрес устройства
    внутри словарь ключи: типы портов
    внутри словарь ключи: состояние портов
    Вызывает функцию 'check_intf_type_status' """
    out_list = []
    out_dict = {}
    out_dict[dev_ip] = {}
    key_type_list = ["phisical", "loopback", "tunnel", "sub"]
    intf_type_dict = dict.fromkeys(key_type_list)
    intf_type_dict["sub"] = {}
    intf_type_dict["phisical"] = {}
    intf_type_dict["loopback"] = {}
    intf_type_dict["tunnel"] = {}
    regex = (r"\n(?P<intf>\S+) +"
             r"(?P<ip>\d+.\d+.\d+.\d+|unassigned) +\S+ +\S+ +"
             r"(?P<status>up|down|administratively down)")
    match = re.finditer(regex, out_ip_int)
    if match:
        for m in match:
            out_list.append(m.groupdict())
        intf_type_dict["sub"] = check_intf_type_status(out_list, ".")
        intf_type_dict["tunnel"] = check_intf_type_status(out_list, "unnel")
        intf_type_dict["loopback"] = check_intf_type_status(out_list, "oopback")
        intf_type_dict["phisical"] = check_intf_type_status(out_list, "thernet")
    out_dict[dev_ip] = intf_type_dict
    return out_dict

def tabl(device, limit=3):
    """ Выводим красивую табличку
    Принимает список словарей с данными для подключения
    и максимальной количество одновременных подключений,
    по умолчанию 3, необязательный параметр.
    Основная функция для вызова кода. В качестве списка словарей
    передается считаный файл yaml с данными для подключения к устройствам.
    Вызывает функцию 'send_show_command_to_devices'
    для отправки команд на несколько устройств"""
#    output_dict = show_ip_int(device)
    output_dict = send_show_command_to_devices(device, limit=limit)
    c = Console()
    t = Table()
    for name in "Device, Port Type, Admin down, Down, Up".split(","):
        t.add_column(name, max_width=22)
    for name, data in output_dict.items():
        t.add_row(
                name, "phisical", '\n'.join(output_dict[name]["phisical"]["admin"]),
                '\n'.join(output_dict[name]["phisical"]["down"]), '\n'.join(output_dict[name]["phisical"]["up"])
                )
        t.add_row(
                None, "loopback", '\n'.join(output_dict[name]["loopback"]["admin"]),
                '\n'.join(output_dict[name]["loopback"]["down"]), '\n'.join(output_dict[name]["loopback"]["up"])
                )
        t.add_row(
                None, "tunnel", '\n'.join(output_dict[name]["tunnel"]["admin"]),
                '\n'.join(output_dict[name]["tunnel"]["down"]), '\n'.join(output_dict[name]["tunnel"]["up"])
                )
        t.add_row(
                None, "subinterface", '\n'.join(output_dict[name]["sub"]["admin"]),
                '\n'.join(output_dict[name]["sub"]["down"]), '\n'.join(output_dict[name]["sub"]["up"])
                )
    c.print(t)
    print("Время выполнения скрипта", datetime.now() - time)
    print(f"Количество одновременных подключений {limit}")
#    tabl_count_port(output_dict)

"""
def tabl_count_port(output_dict):
    c = Console()
    t = Table()
    for name in "Device, Port Type, Admin down, Down, Up".split(","):
        t.add_column(name, max_width=22)

    for name, data in output_dict.items():
        res = counter(output_dict, "phisical")
        if res:
        t.add_row(name, "phisical", ",".join(res[name],
            str(len(output_dict[name]["phisical"]["down"])), str(len(output_dict[name]["phisical"]["up"])))
        t.add_row(None, "loopback", str(l_a), str(l_d), str(l_u))
        t.add_row(None, "tunnel", str(len(output_dict[name]["tunnel"]["admin"])),
            str(len(output_dict[name]["tunnel"]["down"])), str(len(output_dict[name]["tunnel"]["up"])))
        t.add_row(None, "subinterface", str(len(output_dict[name]["sub"]["admin"])),
            str(len(output_dict[name]["sub"]["down"])), str(len(output_dict[name]["sub"]["up"])))
        t.add_row(None, None, None, None, None)
    c.print(t)
    """

def counter(output_dict, port_type):
    count_dict = {}
    count_list = []
    p_a = len(output_dict[name][port_type]["admin"])
    p_u = len(output_dict[name][port_type]["down"])
    p_d = len(output_dict[name][port_type]["up"])
    if p_a + p_u + p_d != 0:
        cout_list.append(p_a)
        cout_list.append(p_d)
        cout_list.append(p_u)
        count_dict[name] = cout_list
        return count_dict
    else: return None



if __name__ == "__main__":
#    print(show_ip_int(device))
    with open("devices_my.yaml") as f:
        devices = yaml.safe_load(f)
    #print(argv[1])
    if len(argv) > 1:
        limit = int(argv[1])
    else:
        limit = 3
    tabl(devices, limit=limit)