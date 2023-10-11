import xlsxwriter

# Create a data array
data = [
    ["Z", 53, "F"],
    ["T", 49, "M"],
    ["A", 55, "F"],
    ["L", 61, "M"],
]

# Sort the data array by column names and row names
data = sorted(data, key=lambda x: x[0]) # sort by name
data = [list(x) for x in zip(*sorted(zip(*data), key=lambda x: x[0]))] # sort by column

# Create an Excel workbook and worksheet
workbook = xlsxwriter.Workbook("table.xlsx")
worksheet = workbook.add_worksheet()

# Get the dimensions of the data array
max_row = len(data)
max_col = len(data[0])

# Create a list of column headers
column_settings = [{"header": col} for col in data[0]]

# Add the table to the worksheet
worksheet.add_table(
    0,
    0,
    max_row - 1,
    max_col - 1,
    {
        "data": data[1:],
        "columns": column_settings,
        "style": "Table Style Light 9",
        "autofilter": False,
    },
)

# Close the workbook
workbook.close()