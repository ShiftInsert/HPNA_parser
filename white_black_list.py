import re
import csv
import sys
import yaml
from pathlib import Path

yaml_config = Path('config.ini')
if not yaml_config.is_file():
    yaml_config = {
        'input_file': 'sh_ip_int_b.csv',
        'delimit': ',',
        'needed_cols': '2 3 9',
        'col_to_parse': '9',
        'whitelist': [],
        'blacklist': ['^$', 'Results:', 'Script', 'root detail', 'sh ip int b'],
        'search_pattern': ' \n ',
        'replace_pattern': '',
        'duplicate': True
    }

    with open('config.ini', 'w') as f:
        yaml.dump(yaml_config, f)

with open('config.ini') as f:
    yaml_config = yaml.load(f)

# print (config)



def filter_by_number(blacklist, col_to_parse, delimit, duplicate, input_file, needed_cols, replace_pattern, search_pattern, whitelist):
    needed_cols = needed_cols.split(' ')
    output_file = input_file.split('.')[0] + '_out.csv'
    
    with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
        reader = csv.reader(csv_input, delimiter = delimit)
        writer = csv.writer(csv_output, quoting=csv.QUOTE_NONNUMERIC)

        for row in reader:
            # print (row)
            new_row = []
            for index, cell_data in enumerate(row):
                if str(index + 1) in needed_cols:
                    if str(index + 1) in col_to_parse:
                        parsed_cell_data = ''
                        for line in cell_data.splitlines():
                            line = white_black_filter(line, whitelist, blacklist)
                            if line:
                                parsed_cell_data = parsed_cell_data + "\n" + line
                        cell_data = parsed_cell_data.strip().replace(search_pattern, replace_pattern).strip()
                    new_row.append(cell_data)

            if duplicate:
                mapped_index = needed_cols.index(col_to_parse)
                if len(new_row[mapped_index].splitlines()) > 1:
                    for item in new_row[mapped_index].splitlines():
                        new_line = []
                        new_line.extend(line[:mapped_index])
                        new_line.append(item)
                        new_line.extend(line[mapped_index + 1:])
                        writer.writerow(new_line)
            else:
                writer.writerow(new_row)

def whitelist_filter(line, whitelist = []):
    ''' filters the text chunk, keeping the lines satisfying any of the whitelist patterns
        !!!EMPTY WHITELIST DOES NOT FILTER ANYTHING AT ALL !!! '''
    
    if any((True if re.search(pattern, line) else False for pattern in whitelist)):
        return line
    else:
        return ''

def blacklist_filter(line, blacklist = []):
    if not any((True if re.search(pattern, line) else False for pattern in blacklist)):
        return line
    else:
        return ''

def white_black_filter(text_to_filter, whitelist, blacklist):
    if whitelist and blacklist:
        return blacklist_filter(whitelist_filter(text_to_filter, whitelist), blacklist)
    elif whitelist:
        return whitelist_filter(text_to_filter, whitelist)
    elif blacklist:
        return blacklist_filter(text_to_filter, blacklist)

if __name__ == '__main__':
    filter_by_number(**yaml_config)
