# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

import ipaddress

def check_if_ip_is_network(ip_address):
    try:
        ipaddress.ip_network(ip_address)
        return True
    except ValueError:
        return False



def convert_ranges_to_ip_list(ip_list):
    correct_ip_list = []
    first_octs = []
    list_ip = []
    start_ip = ""
    end_ip = ""
    for ip in ip_list:
        if check_if_ip_is_network(ip):
            correct_ip_list.append(ip)
        else:
            first_octs = list(ip.split(".")[0:3])
            start_ip = ip.split("-")[0].split(".")[-1]
            if len(ip.split("-")[-1]) > 3:
                end_ip = ip.split("-")[-1].split(".")[-1]
            else:
                end_ip = ip.split("-")[-1]
            #list_ip = list(range(start_ip, end_ip))
            list_ip = list(range(int(start_ip), int(end_ip)+1))
            for last_octs in list_ip:
                 correct_ip_list.append(".".join(first_octs) + "." + str(last_octs))


    return correct_ip_list

if __name__ == "__main__":
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))