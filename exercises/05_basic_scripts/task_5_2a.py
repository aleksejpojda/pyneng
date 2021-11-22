# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску,
как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24, вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000


Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)


Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит
адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28 в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего
в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
ipmask = input("Введите адрес сети и маску: ")
ip = ipmask.split("/")[0].split(".")
mask = ipmask.split("/")[1]
mask_bin = "1" * int(mask) + "0" * (32-int(mask))

ip_bin = format(int(bin(int(ip[0])).split("b")[1]), "08") \
         + format(int(bin(int(ip[1])).split("b")[1]), "08") \
         + format(int(bin(int(ip[2])).split("b")[1]), "08") \
         + format(int(bin(int(ip[3])).split("b")[1]), "08")

ip_net_bin = ip_bin[0:int(mask)] + (32 - int(mask)) * "0"

ip_net = [int(ip_net_bin[0:8], 2), int(ip_net_bin[8:16], 2), \
          int(ip_net_bin[16:24], 2), int(ip_net_bin[24:], 2)]

ip_net_str = str(ip_net[0]) + "." +  str(ip_net[1]) + "." + \
             str(ip_net[2]) + "." +  str(ip_net[3])

print("Network:\n", \
            format(ip_net_str.split(".")[0], "8"), "  ", \
            format(ip_net_str.split(".")[1], "8"), "  ", \
            format(ip_net_str.split(".")[2], "8"), "  ", \
            format(ip_net_str.split(".")[3], "8"), "  ", "\n", \
            format(int(bin(int(ip_net_str.split(".")[0])).split("b")[1]), "08"), "  ", \
            format(int(bin(int(ip_net_str.split(".")[1])).split("b")[1]), "08"), "  ", \
            format(int(bin(int(ip_net_str.split(".")[2])).split("b")[1]), "08"), "  ", \
            format(int(bin(int(ip_net_str.split(".")[3])).split("b")[1]), "08"), "  ", "\n" )
print("Mask:\n", "/"+mask, "\n", \
            format(int(mask_bin[0:8], 2), "<8"), "  ", \
            format(int(mask_bin[8:16], 2), "<8"), "  ", \
            format(int(mask_bin[16:24], 2), "<8"), "  ", \
            format(int(mask_bin[24:], 2), "<8"), "  ", "\n", \
            mask_bin[0:8], "  ", mask_bin[8:16], "  ", \
            mask_bin[16:24], "  ", mask_bin[24:], "  "
           )

