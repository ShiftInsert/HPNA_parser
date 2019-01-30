const_columns = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL AM AN AO AP AQ AR AS AT AU AV AW AX AY AZ'.split(' ')
needed_cols = 'B c H'

needed_cols = [const_columns.index(temp_col.upper()) for temp_col in needed_cols.split(' ')]
print (needed_cols)

if 8 == 8:
    print ('it is')
else:
    print ('no')