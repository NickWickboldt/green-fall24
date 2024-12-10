#Conditionals
# Ways to test if something is true or false

#Conditional operators
# == tests for equality
# != tests for inequality
# >= greater than or equal to 
# <= less than or equal to 

#Conditional statements
# if and else --> elif

if "bob" == "bob":
    print("Bob is here")

if "bob" == "rob":
    print("Bob is not here")

if "bob" != "rob":
    print("Rob is here")

name = input()

if name == "philip":
    print("philip is here")
elif name == "vir":
    print("vir is here")
elif name == "claire":
    print("claire is here")
else:
    print("luis is here")

if name == "mia":
    print("mia is here")
else:
    print("mia is not here")

# Testing multiple conditions
# or
# and

if 5 < 10 and 6 > 3: 
    print("numbers")

if 6 < 2 or 4 < 8:
    print("num")