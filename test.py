import re
search_pattern = ' +'
replace_pattern = '!'
parsed_cell_data = '''13   VL-G-DE-SI03-0002                Myass
16   VL-SIS-SP01-0002                 Myass
24   VL-G-DE-PD03-0002                Myass
100  VL-G-DE-TR14-0002                Myass
271  VL-G-WW-CL05-0002                Myass
301  VL-SIS-SO03-0002                 Myass
443  VL-G-DE-AD12-0002                Myass'''
cell_data = re.sub(search_pattern, replace_pattern, parsed_cell_data.strip())
print ('|' + cell_data + '|')