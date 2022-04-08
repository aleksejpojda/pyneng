from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
import yaml
from itertools import repeat
from pprint import pprint
from sys import argv

device1 = {'device_type': 'cisco_ios',
           "host": "10.48.247.170",
           "username": "dz220883pap",
           "password": "Kolobok11",
            'secret': ''}

def send_show_command_to_devices(devices, command, limit=3):
    """ Подключение на несколько устройств одновременно.
    Принимает в себя список словарей с данными для подключения
    к нескольким устройствам. Лимит по умолчанию 3 устройства.
    Возвращает словарь с выводом устройства """
    out_dict = {}
    with ThreadPoolExecutor(max_workers=limit) as ex:
        result = ex.map(show_command, devices, repeat(command))
    for res in result:
        out_dict.update(res)
    return out_dict


def show_command(device, command):
    """ Отправка команды 'sh ip int br'.
    Принимает в себя словарь с данными для подключения
    Возвращает вывод устройства, строка
    Вызывает функцию 'parse_out' """
#    out_dict = {}
    with ConnectHandler(**device) as sw:
        #        sw.enable()
        out = sw.send_command(command)
    return out

if __name__ == "__main__":
    #    print(show_ip_int(device))
#    with open("devices_my.yaml") as f:
#        devices = yaml.safe_load(f)
    # print(argv[1])
#    if len(argv) > 1:
#        limits = int(argv[1])
#    else:
#        limits = 3
#    pprint(send_show_command_to_devices(device1, "show cdp nei det", limit=5))
#    out = show_command(device1, "show cdp nei det")
#    with open("out_file.yaml", "w") as w:
#        yaml.dump(out, w, default_flow_style=False)
    print(show_command(device1, "show cdp nei det"))
