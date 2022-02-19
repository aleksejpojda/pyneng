# Write your code here :-)

from netmiko import ConnectHandler
import re, yaml
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
from rich.table import Table
from rich.console import Console


device1 = {'device_type': 'cisco_ios',
          "ip": "192.168.100.1",
          "username": "cisco",
          "password": "cisco",
          'secret': 'cisco'}

def send_show_command_to_devices(devices, limit=3):
    out_dict = {}
    with ThreadPoolExecutor(max_workers=limit) as ex:
        result = ex.map(show_ip_int, devices)
    for res in result:
        #print(res)
        out_dict.update(res)
    return out_dict

def send_and_parse_command_parallel(devices, command, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as ex:
        for dev in devices:
            out = ex.submit(show_ip_int, dev, command)

def show_ip_int(device):
    with ConnectHandler(**device) as sw:
#        sw.enable()
        out = sw.send_command("sh ip int br")
        out_dict = parse_out(out, sw.host)
    return out_dict

def check_intf_type_status(list_dict, type_intf):
    list_intf_up = []
    list_intf_down = []
    list_intf_admin = []
    status_dict = {}
    key_status_list = ["up", "down", "admin"]
    status_dict = dict.fromkeys(key_status_list)
    for line in list_dict:
        intf = line['intf']
        if type_intf in intf and line['status'] == "up":
            list_intf_up.append(intf)
        elif type_intf in intf and line['status'] == "down":
            list_intf_down.append(intf)
        elif type_intf in intf and line['status'] == "administratively down":
            list_intf_admin.append(intf)
    status_dict["up"] = list_intf_up
    status_dict["down"] = list_intf_down
    status_dict["admin"] = list_intf_admin
    return status_dict

def parse_out(out_ip_int, dev_ip):
 #   device_ip = dev_ip
    out_list = []
    out_dict = {}
    out_dict[dev_ip] = {}
    key_type_list = ["phisical", "loopback", "tunnel", "sub"]
    intf_type_dict = dict.fromkeys(key_type_list)
    intf_type_dict["sub"] = {}
    intf_type_dict["phisical"] = {}
    intf_type_dict["loopback"] = {}
    intf_type_dict["tunnel"] = {}
    regex = (r"\n(?P<intf>\S+) +"
             r"(?P<ip>\d+.\d+.\d+.\d+|unassigned) +\S+ +\S+ +"
             r"(?P<status>up|down|administratively down)")
    match = re.finditer(regex, out_ip_int)
    if match:
        for m in match:
            out_list.append(m.groupdict())
        intf_type_dict["sub"] = check_intf_type_status(out_list, ".")
        intf_type_dict["tunnel"] = check_intf_type_status(out_list, "unnel")
        intf_type_dict["loopback"] = check_intf_type_status(out_list, "oopback")
        intf_type_dict["phisical"] = check_intf_type_status(out_list, "thernet")
    out_dict[dev_ip] = intf_type_dict
    return out_dict

def tabl(device):
#    output_dict = show_ip_int(device)
    output_dict = send_show_command_to_devices(device)
    c = Console()
    t = Table()
    for name in "Device, Port Type, Admin down, Down, Up".split(","):
        t.add_column(name, max_width=22)
    for name, data in output_dict.items():
        t.add_row(
                name, "phisical", '\n'.join(output_dict[name]["phisical"]["admin"]),
                '\n'.join(output_dict[name]["phisical"]["down"]), '\n'.join(output_dict[name]["phisical"]["up"])
                )
        t.add_row(
                None, "loopback", '\n'.join(output_dict[name]["loopback"]["admin"]),
                '\n'.join(output_dict[name]["loopback"]["down"]), '\n'.join(output_dict[name]["loopback"]["up"])
                )
        t.add_row(
                None, "tunnel", '\n'.join(output_dict[name]["tunnel"]["admin"]),
                '\n'.join(output_dict[name]["tunnel"]["down"]), '\n'.join(output_dict[name]["tunnel"]["up"])
                )
        t.add_row(
                None, "subinterface", '\n'.join(output_dict[name]["sub"]["admin"]),
                '\n'.join(output_dict[name]["sub"]["down"]), '\n'.join(output_dict[name]["sub"]["up"])
                )
    c.print(t)


if __name__ == "__main__":
#    print(show_ip_int(device))


    with open("devices_my.yaml") as f:
        devices = yaml.safe_load(f)
        print(tabl(devices))
    #print(send_show_command_to_devices(devices))