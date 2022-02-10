# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import telnetlib
import time
from task_21_3 import parse_command_dynamic
import re


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
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

    def _send_command(self, command):
        self._write_line(command)
        time.sleep(1)
        out = self.telnet.read_very_eager().decode('utf-8')
        return out

    def send_config_commands(self, config_commands, strict=True):
        out = ""
        self.telnet.write(b"conf t\n")
        if type(config_commands) == str:
            result = self._send_command(config_commands)
            out = self._check_errors(result, config_commands, strict)
            self.telnet.write(b"end\n")
        else:
            for command in config_commands:
                result = self._send_command(command)
                output = self._check_errors(result, command, strict)
                out += output
            self.telnet.write(b"end\n")
        return out

    def _check_errors(self, output_config_commands, comm, strict=True):
        out_err = str(re.findall(r"%.+", output_config_commands))[1:-1]
        if strict == True and "%" in output_config_commands:
            raise ValueError(f'При выполнении команды "{comm}" на устройстве {self.ip} возникла ошибка -> {out_err}')
        elif strict == False and "%" in output_config_commands:
            print(f'При выполнении команды "{comm}" на устройстве {self.ip} возникла ошибка -> {out_err}')
        else:
            return output_config_commands


if __name__ == "__main__":
    r1_params = {
                'ip': '192.168.100.1',
                'username': 'cisco',
                'password': 'cisco',
                'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors+correct_commands
#    print(r1.send_config_commands(commands, strict=True))
    print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'], strict=False))