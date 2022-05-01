from netmiko import ConnectHandler
from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH
import getpass


class Mikrot(MikrotikRouterOsSSH):
    def __init__(self, **kwargs):
        self.ip = device["host"]
        self.port = device["port"]
        self.device_type = device["device_type"]
        self.login = input("Введите имя пользователя: ") + "+ct"
        self.password = getpass.getpass()
        device["username"] = self.login
        device['password'] = self.password
        super().__init__(**device)

    def send_command(self, command, **kwargs):
        out = super().send_command(command)
        return out




#login = input("Введите имя пользователя: ") + "+ct"
#print(login)
#password = getpass.getpass()
device = {'device_type': 'mikrotik_routeros',
           "host": "10.48.51.65",
          "port": "8990",
           "username": "",
           "password": "Djy.xrF1",
           'secret': ''}
"""
def send_command_to_mikrotik(device, command):
    with ConnectHandler(**device) as mik:
        print(f"Подключаюсь к {device['host']}")
        out = mik.send_command(command)
    return out
"""
if __name__ == "__main__":
   m = Mikrot(**device)
   print(m.ip)
   print(m.send_command("sys resou pr"))