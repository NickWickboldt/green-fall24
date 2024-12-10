#Loops
# Loops allow us to execute code multiple times


# for loop
for i in range(10000): # i is for iterator
    print("hello", i)


# # Make a for loop that prints the iterator + 1, 1000 times
# for i in range(1000):
#     print(i + 1)

# # Make a for loop that breaks the computer
# for i in range(100000000000000000000000000000000000000000000):
#     print(i)

#while loop
alive = True
i = 0
while alive:
    i+=1
    print("alive, age: ", i)
    if(i == 100):
        alive = False

#Loop Challenge
# Create a new file named loop_challenge.py

# 1. Create a for loop that counts 5 to 505
# 2. Create a for loop that prints out chr(i) 1000 times
# 3. Create a while loop that depends on the value cooking, the value cooking equals
# false after the iterator i equals -10000, the iterator should count backwards
# 4. Create a while loop that stops at 1000. Inside the while loop is a for loop
#  that prints 0 through 9, i and j
# 5. Create a for loop with range 100 with another for loop inside of it with range 1000
# use i and j, print out j

for j in range(1000):
    print(j)

for i in range(1000):
    print(i)

#nested for loop ~ solution to 5
for i in range(100):
    for j in range(1000):
        print(j)
