# -*- coding: utf-8 -*-
"""
Задание 9.4

Создать функцию convert_config_to_dict, которая обрабатывает конфигурационный
файл коммутатора и возвращает словарь:
* Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
* Если у команды верхнего уровня есть подкоманды, они должны быть в значении
  у соответствующего ключа, в виде списка (пробелы в начале строки надо удалить).
* Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются
с '!', а также строки в которых содержатся слова из списка ignore.

Для проверки надо ли игнорировать строку, использовать функцию ignore_command.

Часть словаря, который должна возвращать функция (полный вывод можно посмотреть
в тесте test_task_9_4.py):
{
    "version 15.0": [],
    "service timestamps debug datetime msec": [],
    "service timestamps log datetime msec": [],
    "no service password-encryption": [],
    "hostname sw1": [],
    "interface FastEthernet0/0": [
        "switchport mode access",
        "switchport access vlan 10",
    ],
    "interface FastEthernet0/1": [
        "switchport trunk encapsulation dot1q",
        "switchport trunk allowed vlan 100,200",
        "switchport mode trunk",
    ],
    "interface FastEthernet0/2": [
        "switchport mode access",
        "switchport access vlan 20",
    ],
}

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from sys import argv
from pprint import pprint
ignore = ["duplex", "alias", "configuration"]


def ignore_command(command, ignore):
    """
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    """

    ignore_status = False
    for word in ignore:
        if word in command:
            ignore_status = True
    return ignore_status

command_up = ""
command_down = []
command = {}

def convert_config_to_dict(config_filename):
    with open(config_filename) as f:
        file = f.read()
        out_dict = {}
        out_dict_line = ""
        for line in file.split("\n"):
            if line:
                if ignore_command(line, ignore) or "!" in line:
                    pass
                else:
                    if line.startswith(" ") == False:
                        out_list = []
                        out_dict[line] = []
                        out_dict_line = line
                    else:
                        out_list.append(line)
                        out_dict[out_dict_line] = out_list
    return out_dict











def convert_config_to_dict_1(config_filename):
    with open(config_filename) as f:
        output = f.read()
        cfg_section = output.replace(" "*9, "").split("!\n")
        for section in cfg_section:
#            command_down = []
#         print(section.split("\n"))
            section_cfg_list = section.split("\n")
#            section_cfg_list = section_cfg_list.lstrip("\n")
#         print("-"*20)
            for line in section_cfg_list:
                line = line.lstrip("\n")
                if line.startswith("!") == False:
                    if line.startswith(" ") == False:
                        if ignore_command(line, ignore) == False:
                            command_up = line
                            command[line] = []
                            command_down = []
                    elif line.startswith(" ") == True:
                        if ignore_command(line, ignore) == False:
                            command_down.append(line.strip())
                    command[command_up] = command_down
#                    print(command)
        del command['']
        return command

pprint(convert_config_to_dict_1("config_sw1.txt"))
pprint(convert_config_to_dict("config_sw1.txt"))
