from command_to_dev import show_command
from textfsm import clitable
from pprint import pprint


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
    for item_val, item_keys in new_dict.items():
        if not new_dict_unique.get(item_val):
            new_dict_unique.update({item_keys: item_val})
    return new_dict_unique

if __name__ == "__main__":
    #print(show_command(device1, "sh cdp nei det"))
    #pprint(parce_out_list_ip
    out = send_and_parse_show_command(device1, "sh cdp nei det")
    first_scan_dict = create_new_small_dict(out, device1["host"])
