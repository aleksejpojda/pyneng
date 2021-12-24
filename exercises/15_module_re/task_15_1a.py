# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re

def get_ip_from_cfg(config):
    ip_intf_list = {}
    ip_list = []
    intf = ""
    regex = r"address (\d.+) (\d.+)"
    regex_intf = r"interface ([A-Z]\S+\d)"
    with open(config) as f:
        for line in f:
            intf = re.search(regex_intf, line)
            m = re.search(regex, line)
            if intf:
                intf_1 = intf.group(1)
            if m:
                ip_list = tuple(m.group(1, 2))
                ip_intf_list[intf_1] = ip_list
    return ip_intf_list

if __name__ == "__main__":
    print(get_ip_from_cfg("config_r1.txt"))