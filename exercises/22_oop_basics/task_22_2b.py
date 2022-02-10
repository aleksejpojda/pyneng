# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
from task_21_3 import parse_command_dynamic


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username')
        self.telnet.write(username.encode("ascii")+b"\n")
        self.telnet.read_until(b'Password')
        self.telnet.write(password.encode("ascii")+b"\n")
        self.telnet.write(b"enable\n")
        self.telnet.read_until(b'Password')
        self.telnet.write(secret.encode("ascii")+b"\n")
        self.telnet.write(b"terminal length 0\n")
        time.sleep(0.5)
        self.telnet.read_very_eager()

    def _write_line(self, line):
        return self.telnet.write(line.encode("utf-8") + b"\n")

    def send_show_command(self, show_command, parse=True, templates = "templates", index = "index"):
        self._write_line(show_command)
        time.sleep(0.5)
        out = self.telnet.read_very_eager().decode('utf-8')
        if parse:
            attrib = {}
            attrib["Command"] = show_command
            out_parse = parse_command_dynamic(out, attrib, index, templates)
            return out_parse
        else:
            return out

    def send_config_commands(self, config_commands):
        self.telnet.write(b"conf t\n")
        if type(config_commands) == str:
            self._write_line(config_commands)
        else:
            for command in config_commands:
                self._write_line(command)
        self.telnet.write(b"end\n")
        time.sleep(0.5)
        out = self.telnet.read_very_eager().decode('utf-8')
        return out

if __name__ == "__main__":
    r1_params = {
                'ip': '192.168.100.1',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    print(r1.send_config_commands("logining 10.1.1.1"))
    print(r1.send_config_commands(['interface loop55', 'a', 'ip address 5.5.5.5 255.255.255.255']))