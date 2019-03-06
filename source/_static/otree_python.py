# Comments start with a # symbol.

####################################################
## 1. Basics
####################################################

# integer
3

# float (floating-point number)
3.14

# Math is what you would expect
1 + 1  # => 2
8 - 1  # => 7
10 * 2  # => 20
35 / 5  # => 7.0

# Enforce precedence with parentheses
(1 + 3) * 2  # => 8

# Boolean Operators
# Note they are
True and False # => False
False or True # => True

# negate with not
not True  # => False
not False  # => True

# Equality is ==
1 == 1  # => True
2 == 1  # => False

# Inequality is !=
1 != 1  # => False
2 != 1  # => True

# More comparisons
1 < 10  # => True
1 > 10  # => False
2 <= 2  # => True
2 >= 2  # => True

# Comparisons can be chained!
1 < 2 < 3  # => True
2 < 3 < 2  # => False

# A string (text) is created with " or '
"This is a string."
'This is also a string.'

# Strings can be added too!
"Hello " + "world!"  # => "Hello world!"

# None means an empty/nonexistent value
None  # => None


####################################################
## 2. Variables, lists, and dicts
####################################################

# print() displays the value in your command prompt window
print("I'm Python. Nice to meet you!") # => I'm Python. Nice to meet you!

# Variables
some_var = 5
some_var  # => 5

# Lists store sequences
li = []

# Add stuff to the end of a list with append
li.append(1)    # li is now [1]
li.append(2)    # li is now [1, 2]
li.append(3)    # li is now [1, 2, 3]

# Access a list like you would any array
# in Python, the first list index is 0, not 1.
li[0]  # => 1
# Assign new values to indexes that have already been initialized with =
li[0] = 42
li # => [42, 2, 3]


# You can add lists
other_li = [4, 5, 6]
li + other_li   # => [42, 2, 3, 4, 5, 6]

# Get the length with "len()"
len(li)   # => 6

# Dictionaries store mappings
empty_dict = {}
# Here is a prefilled dictionary
filled_dict = {
    'name': 'Lancelot',
    'quest': "To find the holy grail",
    'favorite_color': "Blue"
}

# Look up values with []
filled_dict['name']   # => 'Lancelot'

# Check for existence of keys in a dictionary with "in"
'name' in filled_dict   # => True
'age' in filled_dict   # => False

# set the value of a key with a syntax similar to lists
filled_dict["age"] = 30  # now, filled_dict["age"] => 30


####################################################
## 3. Control Flow
####################################################

# Let's just make a variable
some_var = 5

# Here is an if statement.
# prints "some_var is smaller than 10"
if some_var > 10:
    print("some_var is totally bigger than 10.")
elif some_var < 10:    # This elif clause is optional.
    print("some_var is smaller than 10.")
else:           # This is optional too.
    print("some_var is indeed 10.")

"""
SPECIAL NOTE ABOUT INDENTING
In Python, you must indent your code correctly, or it will not work.
All lines in a block of code must be aligned along the left edge.
When you're inside a code block (e.g. "if", "for", "def"; see below),
you need to indent by 4 spaces.

Examples of wrong indentation:

if some_var > 10:
print("bigger than 10." # error, this line needs to be indented by 4 spaces


if some_var > 10:
    print("bigger than 10.")
 else: # error, this line needs to be unindented by 1 space
    print("less than 10")

"""


"""
For loops iterate over lists
prints:
    1
    4
    9
"""
for x in [1, 2, 3]:
    print(x*x)

"""
"range(number)" returns a list of numbers
from zero to the given number MINUS ONE

the following code prints:
    0
    1
    2
    3
"""
for i in range(4):
    print(i)


####################################################
## 4. Functions
####################################################

# Use "def" to create new functions
def add(x, y):
    print('x is', x)
    print('y is', y)
    return x + y

# Calling functions with parameters
add(5, 6)   # => prints out "x is 5 and y is 6" and returns 11


####################################################
## 5. List comprehensions
####################################################

# We can use list comprehensions to loop or filter
numbers = [3,4,5,6,7]
[x*x for x in numbers]  # => [9, 16, 25, 36, 49]

numbers = [3, 4, 5, 6, 7]
[x for x in numbers if x > 5]   # => [6, 7]

####################################################
## 6. Modules
####################################################

# You can import modules
import random
print(random.random()) # random real between 0 and 1

