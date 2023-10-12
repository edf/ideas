import xlsxwriter

workbook = xlsxwriter.Workbook('hidden-rows.xlsx') # create a new excel workbook
worksheet = workbook.add_worksheet()               # add a new worksheet

data = [
    ['a', 'b', 'c', 'd'], # visible row
    ['x', 'x', 'x', 'x'], # hidden row
    ['x', 'y', 'z', 'x'], # visible row
    ['x', 'x', 'x', 'x'], # hidden row
    ['e', 'f', 'g', 'h'], # visible row
]

# write to worksheet
row = 0 # initialize the row index
col = 0 # initialize the column index

for item, cost in (data):                  # loop through each row in the data list
    worksheet.write(row, col,     item[0]) # write the first element of the row to 1st column
    worksheet.write(row, col + 1, item[1]) # write the second element of the row to 2nd column
    worksheet.write(row, col + 2, item[2]) # write the third element of the row to 3rd column
    worksheet.write(row, col + 3, item[3]) # write the fourth element of the row to 4th column
    row += 1 # increment the row index by 1

# hide the rows that have only x characters in each column
for i in range(len(data)):             # loop through each row index
    if all(x == 'x' for x in data[i]): # check if all elements in the row are x characters
        worksheet.set_row(i, None, None, {'hidden': True}) # hide the row using hidden attribute

workbook.close() # save the workbook
