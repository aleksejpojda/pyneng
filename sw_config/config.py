import yaml
from jinja2 import Environment, FileSystemLoader
from sys import argv


def param_from_cmd():
    """Функция обрабатывает параметры на входе комндной строки"""
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
            if len(argv) > argv.index('-t') + 1 and len(argv[argv.index('-t') + 1]) > 3:
                template = argv[argv.index('-t') + 1]
                t = True
            else:
                print("Отсутствует обязательный параметр")
                return
        else:
            t = None
        if '-c' in argv:
            if len(argv) > argv.index('-c') + 1 and len(argv[argv.index('-c') + 1]) > 3:
                config = argv[argv.index('-c') + 1]
                c = True
            else:
                print("Отсутствует обязательный параметр")
                return
        else:
            c = None
        if '-ip' in argv:
            file = True
            ip = True
        else:
            ip = None
        if '-h' in argv:
            print(help_text)
            h = True
        else:
            h = None
        list_param = [t, c, ip, h]
        if not any(list_param):
            print("Что-то не так с параметрами")
            print(help_text)
            return
    return template, config, file

def generate_config(params):
    """Функция генерирует конфиг на основе шаблона и файла данных
    На вход принимает список параметров template - шаблон, config - конфигурация устройства,
    file - какое имя файла исользовать (hostname или ip)"""
    if params:
        template = params[0]
        config = params[1]
        file = params[2]
    else:
        return
    env = Environment(loader=FileSystemLoader("."), lstrip_blocks=True, trim_blocks=True)
    templ = env.get_template(template)
    with open(config, "r") as f:
        conf = yaml.safe_load(f)
    for device in conf:
        if file == True:
            sw = device['ip_vlan_intf'].split()[0] + '.txt' # Берем имя из значение параметра ip_vlan_intf до пробела
        elif file == False:
            sw = device['hostname'] + '.txt' # Берем имя из hostname
        with open(sw, 'w') as f:
            f.write(templ.render(device))
            print(f'Файл {sw} записан')


if __name__ == '__main__':
    generate_config(param_from_cmd())