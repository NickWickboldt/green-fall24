# Classes
# Classes are the foundation of object-oriented programming (OOP).

class Person:
    #constructor
    def __init__(self, name, personality, hair_color, eye_color): #attributes
        self.name = name
        self.personality = personality
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.is_living = False

    def walk(self):
        print(self.name, "is walking")

    def talk(self):
        print(self.name, "says hello")

    def dye_hair(self, new_color):
        self.hair_color = new_color
        print(self.name, "changed their hair color to", new_color)

    def die(self):
        if(self.is_living == True):
            self.is_living = False
            print(self.name, "has died...RIP")

    def born(self):
        self.is_living = True
        print(self.name, "has been born... Yay!")

person1 = Person("Joell", "weird and hyper", "yellow", "rainbow")
person1.walk()
person1.talk()
person1.dye_hair("pink")
person1.die()

#Make a new person, make them walk, make them die
person2 = Person("Unfortunate Soul", "sad", "none", "none")
person2.born()
person2.walk()
person2.die()




# Class Challenge
# 1: Create a new file named class_challenge.py
# 2: Create a Dog class with the attributes breed, fur_color, eye_color, and name
# 3: Create a class function named bark() which makes the dog bark
# 4: Create a class function named fetch() which makes the dog fetch
# 5: Create a class function named vet() which makes the dog go to the vet
# 6: Create a class function named put_down() which does... yk
# 7: Create a class function named bath() which changes the fur color 
# to a light variation
# 8: Create 2 dogs. Make them bark, fetch, go to the vet, take a bath, and be put down