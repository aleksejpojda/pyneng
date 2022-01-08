# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""

import datetime


def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def convert_datetime_to_str(datetime_obj):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")


import re
import csv


def list_dublicate(input_list, number_columns):
    '''
    number_columns номер столбца с нулевого в котором искать повторения
    '''
    for line in input_list:




def write_last_log_to_csv(source_log, output):
    data = {}
    regex = r"(?P<name>.+?),(?P<Email>.+?),(?P<change>\d+.+)"
    with open(source_log) as f:
#        output = f.read()
        reader = csv.DictReader(f)
        for row in reader:
            data.update(row)
        print()
        headers = next(reader)
        headers1 = re.match(r"(?P<Headers>\D+,\D+,\D+ \D+)\n", output.strip("\n"))
        print(headers1.group("Headers"))
        result_list = re.findall(regex, output.strip("\n"))
        for line in result_list:
            data.append(list(match.groups()))
        print(data)

#        print('Headers: ', headers)
#        for row in reader:
#            print(row)
#            result_dict.update(row[1])
#        print(result_dict)
 #       convert_str_to_datetime(line[2])


if __name__ == "__main__":
    print(write_last_log_to_csv("mail_log.csv", "out.txt"))