import yaml
from create_bot import path
import os
from datetime import date, timedelta


def list_dir_sites():
    site = [dir for dir in os.listdir(path) if os.path.isdir(dir) if len(dir.split('_')) == 2]
    return site



def remove_old_files():
    """Удаляет файлы старше трех дней
    Возвращает список файлов"""
    result = {}
    sites = list_dir_sites()
    for site_dir in sites:
        site = site_dir.split('_')[0]
        #print(site, site_dir)
        files = [ f for f in os.listdir(path) if os.path.isfile(f) if f.startswith(site)]
        #print(files)
        for file in files:
            date_in_name = date.fromisoformat(file.split(site)[-1].split('.')[0])
            delta = timedelta(days=2)
            if date_in_name + delta < date.today():
                print(f'старый файл {file}, удаляем')
                os.remove(file)
        result['/'+site_dir] = [ '/'+f for f in os.listdir(path) if os.path.isfile(f) if f.startswith(site)]
    #print(result)
    with open('file_list.yaml', 'w') as f:
        yaml.dump(result, f, default_flow_style=False)

    #return result


#print(list_dir_sites())
#remove_old_files()