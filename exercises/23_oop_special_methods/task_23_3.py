# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
"""

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

topology_example2 = {
    ("R1", "Eth0/4"): ("R7", "Eth0/0"),
    ("R1", "Eth0/6"): ("R9", "Eth0/0"),
}
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        topology_new = {}
        for item_val, item_keys in topology_dict.items():
            if not topology_new.get(item_val):
                topology_new.update({item_keys: item_val})
        return topology_new

    def __add__(self, other):
        sum_dict = {}
        sum_dict.update(self.topology)
        sum_dict.update(other.topology)
        return Topology(sum_dict)

    def delete_link(self, link_from, link_to):
        if link_from == self.topology.keys() and self.topology[link_from] == link_to:
            del self.topology[link_from]
        elif link_to == self.topology.keys() and self.topology[link_to] == link_from:
            del self.topology[link_to]
        else:
            print("Такого соединения нет")

    def delete_node(self, node):
        del_list = []
        for key, val in self.topology.items():
            if node in key or node in val:
                del_list.append(key)
        if del_list:
            for k in del_list:
                del self.topology[k]
        else:
            print("Такого устройства нет")

    def add_link(self,  link_from, link_to):
        port = False
        node = False
        for key, val in self.topology.items():
            if link_from == key and link_to == val:
                node = True
            elif link_to == key and link_from == val:
                node = True
            elif link_from == key or link_to == val:
                port = True
            elif link_to == key or link_from == val:
                port = True
        if port:
            print("Cоединение с одним из портов существует")
        elif node:
            print("Такое соединение существует")
        else:
            self.topology[link_from] = link_to

if __name__=="__main__":
    t = Topology(topology_example)
#    print(t.topology)
#    t.add_link(("R17", "Eth4/0"), ("SW9", "Eth0/7"))
#    print(t.topology)
    t2 = Topology(topology_example2)
    t3 = t+t2
    print(t3.topology)