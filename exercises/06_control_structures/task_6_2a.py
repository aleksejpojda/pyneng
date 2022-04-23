# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
address = input("Введите IP-адрес: ")

if address.count(".") == 3:
    if len(address.split(".")) == 4:
        if address.split(".")[0].isdigit() and address.split(".")[1].isdigit() and address.split(".")[2].isdigit() and address.split(".")[3].isdigit():
            if int(address.split(".")[0]) >= 0 and int(address.split(".")[0]) <= 255:
                if int(address.split(".")[1]) >= 0 and int(address.split(".")[1]) <= 255:
                    if int(address.split(".")[2]) >= 0 and int(address.split(".")[2]) <= 255:
                        if int(address.split(".")[3]) >= 0 and int(address.split(".")[3]) <= 255:
                            if int(address.split(".")[0]) >= 1 and int(address.split(".")[0]) <= 223:
                                print("unicast")
                            elif int(address.split(".")[0]) >= 224 and int(address.split(".")[0]) <= 239:
                                print("multicast")
                            elif address == "255.255.255.255":
                                print("local broadcast")
                            elif address == "0.0.0.0":
                                print("unassigned")
                            else:
                                print("unused")
                        else:
                            print("Неправильный IP-адрес")
                    else:
                        print("Неправильный IP-адрес")
                else:
                    print("Неправильный IP-адрес")
            else:
                print("Неправильный IP-адрес")
        else:
            print("Неправильный IP-адрес")
    else:
        print("Неправильный IP-адрес")
else:
    print("Неправильный IP-адрес")


