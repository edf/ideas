new_list =[]
x_range = range(3, 9)
y_range = range(1, 6)

for i in x_range:
    new_row = [i]
    for j in y_range:
        # print(i)
        # new_column = [j]
        new_row.append(j)
    new_list.append(new_row)
    print("length of row:", len(new_row))

print(new_list)
print("length of array:", len(new_list))
for line in new_list:
    print(line)
