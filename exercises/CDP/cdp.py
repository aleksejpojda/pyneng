from command_to_dev import show_command
from textfsm import clitable
from pprint import pprint
from draw_network_graph import draw_topology


device1 = {'device_type': 'cisco_ios',
           "host": "10.48.247.170",
           "username": "dz220883pap",
           "password": "Kolobok11",
           'secret': ''}
attrib = {'Vendor': 'cisco_ios'}


def parse_command_dynamic(command_output, attributes_dict, index_file="index", templ_path="templates"):
    out_list = []
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    header = list(cli_table.header)
    for row in cli_table:
        out_dict = dict(zip(header, list(row)))
        out_list.append(out_dict)
    return out_list


def parce_net(out_list_dict):
    new_dev = []
    set_list_ip = {line["mngmnt_ip"] for line in out_list_dict}
    for ip in set_list_ip:
        device_all = {'device_type': 'cisco_ios',
                      "username": "dz220883pap",
                      "password": "Kolobok11",
                      'secret': ''}
        device_all["host"] = ip
        new_dev.append(device_all)
    return new_dev


def parce_all_net(new_dev_dict):
    for line in new_dev_dict:
        out_list_dict = send_and_parse_show_command(line, "sh cdp nei det")
        new_dev_dict = []
        if out_list_dict:
            new_dev_dict = (parce_net(out_list_dict))
    return new_dev_dict

def send_and_parse_show_command(device_dict, command):
    #   out = []
    attrib['Command'] = command
    output = show_command(device_dict, command)
    out_cdp_list = (parse_command_dynamic(output, attrib))
    return out_cdp_list

def unique_control(old_set, new_output_cdp_list):
    repeat_scan = False
    unique_ip_set = {lines["mngmnt_ip"] for lines in output_cdp_list}
    new_set = old_set + unique_ip_set
    if len(new_set) > old_set:
        repeat_scan = True
    return repeat_scan

def parce_out_list_ip(output_cdp_list):
    dev_dict_list = []
    if output_cdp_list:
        unique_ip_set = {lines["mngmnt_ip"] for lines in output_cdp_list}
        device_dict = {'device_type': 'cisco_ios',
               "username": "dz220883pap",
               "password": "Kolobok11",
               'secret': ''}
        for line in unique_ip_set:
            device_dict["host"] = line
            dev_dict_list.append(device_dict)
        return dev_dict_list
    else:
        print("Других устройств не найдено")
        return output_cdp_list

def create_new_small_dict(output_from_send_and_parse_list, host_ip):
    new_dict = {}
    for line in output_from_send_and_parse_list:
        new_dict[(host_ip, line["local_port"])] = (line["mngmnt_ip"], line["remote_port"])
    return new_dict

def unique_network_map(new_dict):
    new_dict_unique = {}
    for item_val, item_keys in new_dict[0].items():
        if not new_dict_unique.get(item_val):
            new_dict_unique.update({item_keys: item_val})
    return new_dict_unique



def create_ip_set(dev_dict):
    set_ip_list = {line["host"] for line in dev_dict}
    return set_ip_list

if __name__ == "__main__":
    dev_all_list_dict = []
    dev_list = []
    set_ip_list = {device1["host"]}
    new_set = {}
    a = True
    new_dev = device1
    while a:        # попробовать вынести в функцию
        if type(new_dev) == dict:   # подключились, получили словарь
            out_list_dict = send_and_parse_show_command(new_dev, "sh cdp nei det")
            out = (create_new_small_dict(out_list_dict, new_dev["host"]))
            if dev_list:
                dev_list[0].update(out)
            else: dev_list.append(out)
        elif type(new_dev) == list:
            for line in new_dev:
                out_list_dict = (send_and_parse_show_command(line, "sh cdp nei det"))
                out = create_new_small_dict(out_list_dict, line["host"])
                dev_list[0].update(out)
        if out_list_dict:
            new_dev = parce_net(out_list_dict)  # создали словарь для новых подключений
            for line in new_dev:
                dev_all_list_dict.append(line)
            new_set = create_ip_set(new_dev)    # создали множество айпи адресов
            if len(set_ip_list) != len(set_ip_list | new_set): # если размер не совпал - выполняем по кругу
                set_ip_list = set_ip_list | new_set
                a = True
            else: a = False
        else: a = False
    net_cdp_list = unique_network_map(dev_list)
    draw_topology(net_cdp_list)