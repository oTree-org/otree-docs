# Single line comments start with a number symbol.

""" Multiline strings can be written
    using three "s, and are often used
    as comments
"""

####################################################
## 1. Primitive Datatypes and Operators
####################################################

# You have numbers
3  # => 3

# Math is what you would expect
1 + 1  # => 2
8 - 1  # => 7
10 * 2  # => 20
35 / 5  # => 7

# Enforce precedence with parentheses
(1 + 3) * 2  # => 8

# Boolean Operators
# Note "and" and "or" are case-sensitive
True and False #=> False
False or True #=> True

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

# Strings are created with " or '
"This is a string."
'This is also a string.'

# Strings can be added too!
"Hello " + "world!"  # => "Hello world!"

# A string can be treated like a list of characters
"This is a string"[0]  # => 'T'

# format strings with the format method.
"{} is a {}".format("This", "placeholder")

# None is an object
None  # => None

# Any object can be used in a Boolean context.
# The following values are considered falsey:
#    - None
#    - zero of any numeric type (e.g., 0, 0L, 0.0, 0j)
#    - empty sequences (e.g., '', [])
#    - empty containers (e.g., {})
# All other values are truthy (using the bool() function on them returns True).
bool(0)  # => False
bool("")  # => False


####################################################
## 2. Variables and Collections
####################################################

# Python has a print statement
print("I'm Python. Nice to meet you!") # => I'm Python. Nice to meet you!

# No need to declare variables before assigning to them.
some_var = 5    # Convention is to use lower_case_with_underscores
some_var  # => 5

# incrementing and decrementing a variable
x = 0
x += 1  # Shorthand for x = x + 1
x -= 2  # Shorthand for x = x - 2


# Lists store sequences
li = []
# You can start with a prefilled list
other_li = [4, 5, 6]

# Add stuff to the end of a list with append
li.append(1)    # li is now [1]
li.append(2)    # li is now [1, 2]
li.append(3)    # li is now [1, 2, 3]

# Access a list like you would any array
li[0]  # => 1
# Assign new values to indexes that have already been initialized with =
li[0] = 42
li[0]  # => 42
li[0] = 1  # Note: setting it back to the original value
# Look at the last element
li[-1]  # => 3

# You can look at ranges with slice syntax.
# (It's a closed/open range.)
other_li[1:3]  # => [5, 6]
# Omit the beginning
other_li[1:]  # => [5, 6]
# Omit the end
other_li[:2]  # => [4, 5]

# You can add lists
li + other_li   # => [1, 2, 3, 4, 5, 6]
# Note: values for li and for other_li are not modified.

# Check for existence in a list with "in"
1 in li   # => True

# Examine the length with "len()"
len(li)   # => 6



# Dictionaries store mappings
empty_dict = {}
# Here is a prefilled dictionary
filled_dict = {"one": 1, "two": 2, "three": 3}

# Look up values with []
filled_dict["one"]   # => 1

# Check for existence of keys in a dictionary with "in"
"one" in filled_dict   # => True
1 in filled_dict   # => False

# Looking up a non-existing key is a KeyError
# filled_dict["four"]   # raises KeyError!

# set the value of a key with a syntax similar to lists
filled_dict["four"] = 4  # now, filled_dict["four"] => 4


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
(Python is different from some other languages in this regard)
All lines in a block of code must be aligned along the left edge
When starting a code block (e.g. "if", "for", "def"; see below), you should indent by 4 spaces.
When ending a code block, you should unindent by 4 spaces.

Examples of improperly indented code:

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
    dog is a mammal
    cat is a mammal
    mouse is a mammal
"""
for animal in ["dog", "cat", "mouse"]:
    # You can use {} to interpolate formatted strings. (See above.)
    print("{} is a mammal".format(animal))

"""
"range(number)" returns a list of numbers
from zero to the given number
prints:
    0
    1
    2
    3
"""
for i in range(4):
    print(i)

"""
"range(lower, upper)" returns a list of numbers
from the lower number to the upper number
prints:
    4
    5
    6
    7
"""
for i in range(4, 8):
    print(i)


####################################################
## 4. Functions
####################################################

# Use "def" to create new functions
def add(x, y):
    print("x is {} and y is {}".format(x, y))
    return x + y    # Return values with a return statement

# Calling functions with parameters
add(5, 6)   # => prints out "x is 5 and y is 6" and returns 11

# Another way to call functions is with keyword arguments
add(y=6, x=5)   # Keyword arguments can arrive in any order.


# We can use list comprehensions to loop or filter
[add(i, 10) for i in [1, 2, 3]]  # => [11, 12, 13]
[x for x in [3, 4, 5, 6, 7] if x > 5]   # => [6, 7]

####################################################
## 5. Modules
####################################################

# You can import modules
import random
import math
print(math.sqrt(16))  # => 4

# You can get specific functions from a module
from math import ceil, floor
print(ceil(3.7))  # => 4.0
print(floor(3.7))   # => 3.0

# Python modules are just ordinary python files. You
# can write your own, and import them. The name of the
# module is the same as the name of the file.

####################################################
## 6. Classes
####################################################

# classes let you model complex real-world entities

class Mammal(object):

    # A class attribute. It is shared by all instances of this class
    classification = "Mammalia"
    
    # A method called "set_age" that sets the age of an individual mammal
    # Methods are basically functions that belong to a class.
    # All methods take "self" as the first argument
    def set_age(self):
        self.age = 0
            
    # method that returns True or False
    def older_than_10(self):
        return self.age > 10

    # method with argument
    def predict_age(self, years):
        return 'In {} years I will be {}'.format(years, self.age + years)

        
class Dog(Mammal):
    classification = "Canis lupus"
    
    def bark(self):
        return "woof!"
    

Mammal.classification

# Instantiate a class
lassie = Dog()
lassie.classification # => "Canis lupus"
lassie.set_age()
lassie.older_than_10() # => False
lassie.age = 11
lassie.older_than_10() # => True
lassie.bark() # => "woof!"

