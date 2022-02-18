# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enable()

    def send_command(self, command):
        out = super().send_command(command)
        return self._check_error_in_command(out, command)

    def send_config_set(self, conf_command):
        out = super().send_config_set(conf_command)
        return self._check_error_in_command(out, conf_command)

    def _check_error_in_command(self, output, command):
        errors = [
                "Invalid input detected",
                "Incomplete command",
                "Ambiguous command"
                 ]
        for error in errors:
            if error in output:
                raise ErrorInCommand(
                f'При выполнении команды "{command}" '
                f'на устройстве {self.host} возникла ошибка "{error}"'
                )
        else:
            return output

if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    print(r1.send_config_set('h ip int br'))