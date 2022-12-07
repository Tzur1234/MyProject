class Animal:
    def __init__(self):
        print("Animal Was Created")
    def who_i_am(self):
        print("I am animal")
    def eat(self):
        print("i am eating")





class Dog(Animal):

    species = 'memmal'

    def __init__(self,mybreed, name):
        #initial Animal object !
        Animal.__init__(self)
        self.breed = mybreed
        self.name = name

        print("Dog Created")

    def bark(self, number):
        for i in range(0,number):
            print("Woof ! my name is {}".format(self.name))

##########################
class Circle:

    pi = 3.14

    def __init__(self, radius):
        self.radius = radius
    
    def get_circumfernce(self):
        return self.radius * self.pi * 2

class Book():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"{self.b}"
























