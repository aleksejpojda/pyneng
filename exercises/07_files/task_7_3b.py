# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

a = True
while a:
    vlan = input("Введите номер Vlan:")
    if vlan.isdigit():
        a = False
    else: print("Vlan должен быть числом")

with open("CAM_table.txt") as f:
    res_list = [[int(line.strip().split()[0]), line.strip().split()[1], line.strip().split()[3]]
                 for line in f.readlines() if line.strip() if line.strip().split()[0].isdigit()]
    res_list = sorted(res_list)
    vlan_list = sorted({line[0] for line in res_list})
    if int(vlan) in vlan_list:
        for line in res_list:
            if int(vlan) == line[0]:
                print("{:<10} {:<20} {:<5}".format(line[0], line[1], line[2]))
    else: print(f"Vlan {vlan} не найден")