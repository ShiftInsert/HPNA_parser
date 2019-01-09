import yaml
import _collections_abc
from os import stat
from pathlib import Path

def config_init():
    '''Initializes or reads config.ini file'''
    yaml_hardcode = {
        'input_file': 'show_vlan_br.csv',
        'delimit': ',',
        'needed_cols': '2 3 9',
        'col_to_parse': '9',
        'whitelist': ['Result'],
        'blacklist': ['^$', 'Results:'],
        'search_pattern': ' +',
        'replace_pattern': ' ',
        'duplicate': False
    }
    yaml_file = Path('config.ini')
    status_message = 'CONFIG LOADED'
    # Check for absent or empty file and reinitialize the file and dictionary if needed
    if not yaml_file.is_file() or stat('config.ini').st_size == 0:
        status_message = '*** ABSENT OR ZERO LENGTH CONFIG, REGENERATED ***'
        with open('config.ini', 'w') as f:
            yaml.dump(yaml_hardcode, f)
    with open('config.ini') as f:
        yaml_config = yaml.load(f)
        
    # check if yaml_config is a dict and all needed keys are present in the dict argument
    if not isinstance(yaml_config, _collections_abc.Mapping) or not yaml_config.keys() >= yaml_hardcode.keys():
        status_message = '*** CORRUPT CONFIG, REGENERATED ***'
        with open('config.ini', 'w') as f:
            yaml.dump(yaml_hardcode, f)
        with open('config.ini') as f:
            yaml_config = yaml.load(f)
        
    return yaml_config, status_message

def config_w(yaml_config):
    yaml_hardcode = {
        'input_file': 'search_result_1.csv',
        'delimit': ',',
        'needed_cols': '2 3 9',
        'col_to_parse': '9',
        'whitelist': ['Result'],
        'blacklist': ['^$', 'Results:'],
        'search_pattern': ' +',
        'replace_pattern': ' ',
        'duplicate': False
    }
    # CHECK IF ALL NEEDED KEYS ARE PRESENT IN THE DICT ARGUMENT
    if not yaml_config.keys() >= yaml_hardcode.keys():
        status_message = '*** CONFIG KEYS INCORRECT/MISSING ***'
        return status_message
    with open('config.ini', 'w') as f:
        yaml.dump(yaml_config, f)
        status_message = 'CONFIG SAVED'
        return status_message

if __name__ == '__main__':
    print (config_init())