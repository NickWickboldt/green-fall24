#Challenge
#Make a new file named conditional_challenge.py in the python_basics folder


# 1. The user will enter their age.
# 2. If the user is a child (<=9), call them a child.
# 3. If the user is a tween (10 < 13), call them annoying.
# 4. If the user is a teenager (13 < 20), call them skibidi.
# 5. If the user is a adult (> 19), call them super cool
# 6. If the user is a senior (> 59), call them old and quiz them on brainrot.
# 7. If the user is 0, they are dead, let them know.
# 8. If the user is specifically 12 or 19, call them babies.

print("hi, how old are you")
age = input()
age = int(age)

if age == 0:
    print("you are dead")
elif age == 12 or age == 19:
    print("you are baby")
elif age < 10:
    print("you are child")
elif age > 9 and age < 13:
    print("you are annoying")
elif age > 12 and age < 20:
    print("you are boring")
elif age > 19 and age < 60:
    print("you are super cool")
elif age > 59:
    print("what is mewing?")
