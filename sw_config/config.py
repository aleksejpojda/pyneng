import yaml
from jinja2 import Environment, FileSystemLoader
from sys import argv

#print(len(argv))

def param_from_cmd():
    if len(argv) == 1:
        template = 'sw_config.txt'
        config = 'sw_data.yaml'
        print("-t выбрать шаблон для настройки, по-умолчанию sw_config.txt\n"
              "-c выбрать файл с конфигурацией свитча, по-умолчанию sw_data.yaml\n"
              "-h вывод этой справки")
#        print('Нет параметров')
    elif len(argv) == 2:
        print("-t выбрать шаблон для настройки, по-умолчанию sw_config.txt\n"
              "-c выбрать файл с конфигурацией свитча, по-умолчанию sw_data.yaml\n"
              "-h вывод этой справки")
        return
    elif len(argv) == 3:
#        print('Только первый параметр')
        if '-t' in argv[1]:
            template = argv[2]
            config = 'sw_data.yaml'
        elif '-c' in argv[1]:
            config = argv[2]
            template = 'sw_config.txt'
        else:
            print("Что-то не так с параметрами")
            print("-t выбрать шаблон для настройки, по-умолчанию sw_config.txt\n"
                  "-c выбрать файл с конфигурацией свитча, по-умолчанию sw_data.yaml\n"
                  "-h вывод этой справки")
            return
    elif len(argv) > 3:
        if '-t' in argv and '-c' in argv:
            template = argv[argv.index('-t')+1]
            config = argv[argv.index('-c')+1]
        else:
            print("Что-то не так с параметрами")
            return
    return template, config

def generate_config(params):
    if params:
        template = params[0]
        config = params[1]
    else: return
    env = Environment(loader=FileSystemLoader("."))
    templ = env.get_template(template)
    with open(config, "r") as f:
        conf = yaml.safe_load(f)
    for device in conf:
        #sw = device['ip_vlan_intf'].split()[0] + '.txt'    # Берем имя из значение параметра ip_vlan_intf до пробела
        sw = device['hostname'] + '.txt'    # Берем имя из hostname
        with open(sw, 'w') as f:
            f.write(templ.render(device))
            print(f'Файл {sw} записан')


if __name__ == '__main__':
    generate_config(param_from_cmd())