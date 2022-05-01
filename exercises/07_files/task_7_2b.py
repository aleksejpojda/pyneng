# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv
ignore = ["duplex", "alias", "configuration"]


with open(argv[1]) as f:
    with open(argv[2], "w") as w:
        for line in f:
            good_line = False
            for word in ignore:
                if word in line:
                    good_line = True
                    break
            if "!" not in line:
                if good_line == False:
                    w.write(line.rstrip())
                    w.write("\n")