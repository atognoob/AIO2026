'''
<div align="center">

</div>

'''

# Creating a tuple
person = ("name", 24, "AIO")

# Accessing elements (same as lists)
print(person[0])  # Output: name

# Tuples are immutable

# Unpacking a tuple
name, age, occupation = person
print(age)  # Output: 24
# Creating a single-item tuple (note the comma)
single_tuple = (42,)

# Tuple methods
coordinates = (10, 20, 10, 30)
print(coordinates.count(10))  # Output: 2
print(coordinates.index(20))  # Output: 1