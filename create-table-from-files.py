"""
desired output:

column,list1,list2,list3
c1,x,-,x
c2,x,-,-
c3,x,x,-

"""

import os

list_of_files = []
list_of_columns = []
items = []
for filename in os.listdir("."):
    if filename.startswith("list"):
        list_of_files.append(filename)
        list_of_columns.append(filename.split(".", 1)[0])
        try:
            with open(filename, encoding='utf8')as f:
                for line in f:
                    items.append(line.strip())
        except FileNotFoundError:
            print(f"file {filename} does not exist")

contents = sorted(set(items))
print(f"\nsorted, unique list - {contents}\n--\n\n")

new_items = []

print('column', end='')
for line in list_of_columns:
    print(f',{line}', end='')

for content_raw in contents:
    content = content_raw.strip()
    print(f'\n{content}\t', end='')
    for filename2 in list_of_files:
        # print(f'\tfile: {filename2.strip()}', end='')
        try:
            with open(filename2, encoding='utf8')as f:
                new_list = []
                for file_line in f:
                    new_list.append(file_line.strip())
                    # print(f'\tfile_line:  {file_line.strip()}', end='')
                    # print(f'\t
                    # new list: {new_list}')
                if content in new_list:
                    # print(f',{content}', end='')
                    print(f'\tx', end='')
                else:
                    print('\t-', end='')
        except FileNotFoundError:
            print(f"file {filename2} does not exist")
        else:
            pass
            # print(new_list)
print('\n')
print('------------------')
