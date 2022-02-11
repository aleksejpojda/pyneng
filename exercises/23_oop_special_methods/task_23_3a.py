# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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
        self.items = [tuple(item) for item in topology_dict.items()]
        self._index = 0

    def _normalize(self, topology_dict):
        topology_new = {}
        for item_val, item_keys in topology_dict.items():
            if not topology_new.get(item_val):
                topology_new.update({item_keys: item_val})
        return topology_new

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.items):
            current_node = self.items[self._index]
            self._index += 1
            return current_node
        else:
            raise StopIteration

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
    #print(t.topology)
    #t.add_link(("R17", "Eth4/0"), ("SW9", "Eth0/7"))
    #print(t.topology)
    for link in t:
        print(link)