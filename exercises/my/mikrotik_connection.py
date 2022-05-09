from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH
import getpass
from textfsm import clitable
from pprint import pprint
import time


class Mikrot(MikrotikRouterOsSSH):
    def __init__(self, **kwargs):
        self.ip = device["host"]
        self.port = device["port"]
        self.device_type = device["device_type"]
        #self.login = input("Введите имя пользователя: ") + "+ct" # запрос логина при создании экземпляра класса
        #self.password = getpass.getpass() # запрос пароля при создании экземпляра класса
        #device["username"] = self.login    #сохранение лоигна и пароля
        #device['password'] = self.password
        super().__init__(**device)

    def send_command(self, command, **kwargs):
        """
        отправка команд на микротик
        """
        out = super().send_command(command)
        return out

    def reboot_ut(self, intf, **kwargs):
        """
        для перезагрузки модема УТ, пока не осилил
        """
        command1 = "sys telnet 192.168.1.1 routing-table=VRF-{}".format(intf)
        pprint(command1)
        command2 = "sys reb"
        super().send_command(command1)
        #print(out1)
        time.sleep(1)
        super().send_command("admin")
        #print(out3)
        #print("Заходим на модем")
        #print(out1)
        time.sleep(3)
        out2 = self.send_command(command2)
        print(out2)
        return print(f"Команда отправлена на интерфейс {intf}")






#login = input("Введите имя пользователя: ") + "+ct"
#print(login)
#password = getpass.getpass()
device = {'device_type': 'mikrotik_routeros',
           "host": "10.48.51.65",
           "port": "8990",                              # словарь для подключения к устройству
           "username": "dz220883pap+ct",        # +ct необходимо добавлять к имени пользователя
           "password": "Djy.xrF1"               # иначе не будет работать с микротиком
           }
attrib = {'Vendor': 'mikrotik_routeros'} # словарь с атрибутами для парсинга вывода команд
"""
def send_command_to_mikrotik(device, command):
    with ConnectHandler(**device) as mik:
        print(f"Подключаюсь к {device['host']}")
        out = mik.send_command(command)
    return out
"""

def parse_command_dynamic(command_output, attributes_dict, index_file="index", templ_path="templates"):
    """
    парсит вывод с роутеров согласно шаблонам и командам, им сопоставленным
    в файле index. Возвращает словарь
    """
    out_list = []
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    header = list(cli_table.header)
    for row in cli_table:
        out_dict = dict(zip(header, list(row)))
        out_list.append(out_dict)
    return out_list


def parce_int_pr(out_dict):
    """
    Получает словарь со списком интерфесов от функуии parse_command_dynamic
    Удаляет лишние подключения (tmp_ap), пересоздает запись об активном канале
    в формате status: main|reserve
    Изменяет статус интерфейсов на более понятный (Running, Not connected и т.д.)
    Возвращает словарь
    """
    for line in out_dict:
        if line["intf"] == ";;;":
            out_dict.remove(line)
        elif line["intf"].startswith(";;; "):
            result = line["intf"].split()[-2] + " " + line["intf"].split()[-1]
            result = result.replace("(", "").strip(")")
            out_dict.remove(line)
            new_dict = {}
            new_dict["intf"] = result.split()[-1]
            new_dict["status"] = result.split()[0]
            out_dict.append(new_dict)
    for line in out_dict:
        if line["status"] == " R ":
            line["status"] = "Running"
        elif line["status"] == " RS":
            line["status"] = "Running slave"
        elif line["status"] == "  S":
            line["status"] = "Slave, not connected"
        elif line["status"] == "   ":
            line["status"] = "Not connected"
        elif line["status"] == " X ":
            line["status"] = "Disabled port"
    return out_dict

def search_ut_intf(out_dict_new):
    if out_dict_new[-1]["intf"] == "ether1":
        intf = "ether2"
        return intf
    else:
        intf = "ether1"
        return intf

def int_and_ip(out_ip_dict, out_intf_dict):
    """
    По сути функция ищет в одном словаре имена интерфейсов
    и добавляет из другого словаря ip-адреса этих интерфейсов.
    Объединяет 2 словаря с общими ключами
    """
    for line_ip in out_ip_dict:
        for line_intf in out_intf_dict:
            if line_intf["intf"] in line_ip["intf"]:
                line_intf["ip"] = line_ip["ip"]
    return out_intf_dict



if __name__ == "__main__":
    m = Mikrot(**device)
    #print(m.ip)
    out_ip = m.send_command("ip addr pr")
    attrib["Command"] = "ip addr pr" # для поиска в index-файле шаблона, сопоставленного команде
    out_ip_dict = parse_command_dynamic(out_ip, attrib) # парсит вывод списка IP-адресов и создает словарь

    out_intf = m.send_command("int pr")
    attrib["Command"] = "int pr" # для поиска в index-файле шаблона, сопоставленного команде
    out_intf_dict = parse_command_dynamic(out_intf, attrib) # парсит вывод списка интерфейсов и создает словарь
    out_dict_new = parce_int_pr(out_intf_dict) # перестраивает словарь списка интерфейсов
    result_ip_int_dict = int_and_ip(out_ip_dict, out_dict_new) # добавляет в словарь списка интерфейсов ip-адреса
    pprint(result_ip_int_dict)

    #intf = search_ut_intf(out_dict_new)
    #print(intf)
    #m.reboot_ut(intf)
