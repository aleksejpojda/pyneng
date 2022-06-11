import yaml
from jinja2 import Environment, FileSystemLoader
from sys import argv

#print(len(argv))

def param_from_cmd():
    template = 'sw_config.txt'
    config = 'sw_data.yaml'
    file = False
    help_text = ("-t выбрать шаблон для настройки, по-умолчанию sw_config.txt\n"
              "-c выбрать файл с конфигурацией свитча, по-умолчанию sw_data.yaml\n"
              "-h вывод этой справки\n"
              "-ip имя файла берем из hostname\n")
    if len(argv) == 1:
        print(help_text, "Используются значения по-умолчанию")
    elif len(argv) >= 2:
        if '-t' in argv:
            template = argv[argv.index('-t') + 1]
        elif '-c' in argv:
            config = argv[argv.index('-c') + 1]
        elif '-ip' in argv:
            file = True
        elif '-h' in argv:
            print(help_text)
        else:
            print("Что-то не так с параметрами")
            print(help_text)
            return
    return template, config, file

def generate_config(params):
    if params:
        template = params[0]
        config = params[1]
        file = params[2]
    else: return
    env = Environment(loader=FileSystemLoader("."), lstrip_blocks=True, trim_blocks=True)
    templ = env.get_template(template)
    with open(config, "r") as f:
        conf = yaml.safe_load(f)
    for device in conf:
        if file == True:
            sw = device['ip_vlan_intf'].split()[0] + '.txt' # Берем имя из значение параметра ip_vlan_intf до пробела
        elif file == False:
            sw = device['hostname'] + '.txt'    # Берем имя из hostname
        with open(sw, 'w') as f:
            f.write(templ.render(device))
            print(f'Файл {sw} записан')


if __name__ == '__main__':
    generate_config(param_from_cmd())