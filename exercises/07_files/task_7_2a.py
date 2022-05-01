# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv
ignore = ["duplex", "alias", "configuration"]


#with open(argv[1]) as f:
with open("config_sw1.txt") as f:
    for line in f:
        good_line = False
        for word in ignore:
            if word in line:
                good_line = True
                break
        if "!" not in line:
            if good_line == False:
                print(line.rstrip())



"""
from sys import argv
config_file = argv[1]
ignore = ["duplex", "alias", "configuration"]

#result = None
with open(config_file) as f:
    for line in f:
        line=line.rstrip()
        if not line.startswith("!"):
            result = False
            for word in ignore:
                if word in line:
                    result = True
                    break
            if result == False:
                print(line)
"""