# Read in the data
with open('p067_triangle.txt', 'r') as file:  # File contains 100 rows
    data = file.readlines()

# Condition the data
for i in range(len(data)):
    data[i] = list(map(int, data[i].split(' ')))

# Find the max path
for i in reversed(range(len(data) - 1)):  # iter 98-0
    for j in range(len(data[i])):  # iter 0-(length of each line)
        data[i][j] += max(data[i + 1][j], data[i + 1][j + 1])

print(data[0])