#Functions
# Functions do a job for us, or a task
# They can do it multiple times

# Create a function with def
# 2 parts to a function --> function definition and function call

def printSomething(something): #function definition | something = parameter
    print(something)

printSomething("hello") #function call | "hello" = argument

def printTwoThings(first,second): #function definition
    print(first)
    print(second)

printTwoThings("Hello", "World") #function call

#Challenge

# 0. Create a new python file: calculator.py
# 1. Create a 5 function calculator (+-*/%)
# 2. Create a function that counts to 100 (use a for loop)
# 3. Create a function that multiplies 3 numbers and also makes you sad

def counter():
    for i in range(101):
        print(i)

counter()