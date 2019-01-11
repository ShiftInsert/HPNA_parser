import re
import csv
import config_rw
import sys

def col_num_parser(blacklist, col_to_parse, delimit, duplicate, input_file, needed_cols, replace_pattern, search_pattern, whitelist):
    needed_cols = needed_cols.split(' ')
    output_file = input_file.split('.')[0] + '_out.csv'
    
    with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
        reader = csv.reader(csv_input, delimiter = delimit)
        writer = csv.writer(csv_output, quoting=csv.QUOTE_NONNUMERIC)
        
        for row in reader:
            if row:
                new_row = []
                # take each cell in the current row and see if stays and needs to be parsed
                for index, cell_data in enumerate(row):
                    # if current cell index is in "Needed columns" - this cell stays or is parsed later
                    if str(index + 1) in needed_cols:
                        # if current cell index is in "Column to parse" - this cell is parsed and run through filters
                        if str(index + 1) in col_to_parse:
                            parsed_cell_data = ''
                            for line in cell_data.splitlines():
                                line = white_black_filter(line, whitelist, blacklist)
                                if line:
                                    parsed_cell_data = parsed_cell_data + "\n" + line
                            cell_data = parsed_cell_data.strip().replace(search_pattern, replace_pattern).strip()
                        new_row.append(cell_data)
                # Nijat mode code
                if duplicate:
                    mapped_index = needed_cols.index(col_to_parse)
                    try:
                        multiline = new_row[mapped_index].splitlines()
                    except IndexError:
                        sys.exit()
                    if len(multiline) > 1:
                        for item in multiline:
                            new_line = []
                            new_line.extend(new_row[:mapped_index])
                            new_line.append(item)
                            new_line.extend(new_row[mapped_index + 1:])
                            writer.writerow(new_line)
                else:
                    writer.writerow(new_row)

def whitelist_filter(line, whitelist = []):
    ''' filters the text chunk, keeping the lines satisfying any of the whitelist patterns
        !!!EMPTY WHITELIST DOES NOT FILTER ANYTHING AT ALL !!! '''
    # print('entered whitelist_filter()')
    if any((True if re.search(pattern, line) else False for pattern in whitelist)):
        return line
    else:
        return ''

def blacklist_filter(line, blacklist = []):
    ''' filters the text chunk, removing the lines satisfying any of the blacklist patterns'''
    # print('entered blacklist_filter()')
    if not any((True if re.search(pattern, line) else False for pattern in blacklist)):
        return line
    else:
        return ''

def white_black_filter(text_to_filter, whitelist, blacklist):
    # print('entered white_black_filter()')
    if whitelist and blacklist:
        return blacklist_filter(whitelist_filter(text_to_filter, whitelist), blacklist)
    elif whitelist:
        return whitelist_filter(text_to_filter, whitelist)
    elif blacklist:
        return blacklist_filter(text_to_filter, blacklist)

if __name__ == '__main__':
    col_num_parser(**config_rw.config_init()[0])
