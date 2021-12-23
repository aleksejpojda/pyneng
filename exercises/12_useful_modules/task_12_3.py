# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""

from tabulate import tabulate
#reacheble_list = ['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128']
#unreacheble_list = ['172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

def print_ip_table(reacheble_list, unreacheble_list):
    ip_dict = {}
    ip_dict = dict.fromkeys(["Reachable"], reacheble_list)
    d = {"Unreachable": unreacheble_list for ip in unreacheble_list}
    ip_dict.update(d)
    return print(tabulate(ip_dict, headers="keys"))


if __name__ == "__main__":
    print_ip_table(reacheble_list, unreacheble_list)