# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        topology_new = {}
        for item_val, item_keys in topology_dict.items():
            if not topology_new.get(item_val):
                topology_new.update({item_keys: item_val})
        return topology_new

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
    print(t.topology)
    t.add_link(("R17", "Eth4/0"), ("SW9", "Eth0/7"))
    print(t.topology)