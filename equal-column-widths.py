data = [
    [1, 22, 333],
    [4444, 55555, 666666],
    [7777777, 88888888, 999999999]
]
headers = ["Column-Aaaaaaa", "Col-Bbbbb", "Col-C"]

# Calculate the maximum width for each column
column_widths = [max(len(header), max(len(str(item)) for item in column)) for header, column in zip(headers, zip(*data))]

# Initialize a running counter for total column width
total_width = 0

# Print the value for each column
for header, width in zip(headers, column_widths):
    print(f"{header:{width}}", end="  ")
    total_width += width
print()  # Print a newline

# Print the total column width
print(f"Total column width: {total_width + 4}")
print("-" * (total_width + 4 ))


for row in data:
    for item, width in zip(row, column_widths):
        print(f"{item:{width}}", end="  ")
    print()  # Print a newline
