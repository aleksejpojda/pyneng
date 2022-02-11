# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress:
    def __init__(self, ip_mask):
        self.ip = self._check_ip(ip_mask)
        self.mask = int(self._check_mask(ip_mask))

    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"

    def _check_ip(self, ip_mask):
        ip = ip_mask.split('/')[0]
        for octet in ip.split('.'):
            if octet.isdigit() and int(octet) >=0 and int(octet) <= 255:
                self.ip = ip
            else:
                raise ValueError("Incorrect IPv4 address")
        return self.ip

    def _check_mask(self, ip_mask):
        mask = ip_mask.split('/')[1]
        if mask.isdigit() and int(mask) >= 8 and int(mask) <= 32:
            self.mask = mask
        else:
            raise ValueError("Incorrect mask")
        return mask


if __name__ == "__main__":
    ip1 = IPAddress("10.1.1.1/24")
    print(ip1.ip)
    print(ip1.mask)
    print(str(ip1))
    ip_list = []
    ip_list.append(ip1)
    print(ip_list)