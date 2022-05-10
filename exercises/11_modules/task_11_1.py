# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент
вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое
файла в строку, а затем передать строку как аргумент функции (как передать вывод
команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция должна
работать и на других файлах (тест проверяет работу функции на выводе
из sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from pprint import pprint


def parse_cdp_neighbors(command_output):
    out = {}
    for line in command_output.split("\n"):
        if line.strip():
            if ">" in line:
                local_r = line.split(">")[0]
            elif len(line.split()[0]) > 1 and line.split()[0][1].isdigit():
                remote_r = line.split()[0]
                remote_port = line.split()[-2] + line.split()[-1]
                local_port = line.split()[1] + line.split()[2]
                out[(local_r, local_port)] = (remote_r, remote_port)
    return out












def parse_cdp_neighbors_1(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """

    dev_from = ""
    dev_int_from = ()
    dev_int_to = ()
    dev_int_result = {}
    for line in command_output.split("\n"):
        if line.strip():
            if not line.find(">") == -1:
                dev_from = line.split(">")[0]
            elif line[-1].isdigit():
                dev_int_from = (dev_from, line.split()[1] +  line.split()[2])
                dev_int_to = (line.split()[0], line.split()[-2] +  line.split()[-1])
                dev_int_result[dev_int_from] = dev_int_to
    return dev_int_result


if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        pprint(parse_cdp_neighbors(f.read()))