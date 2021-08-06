import inquirer
import random
import datetime

#Program title
txt = ("Waikato Air Email Text Generator")
x = txt.title()
print(x)
#I decided to use " " instead of "\n" because "\n" made a larger gap between the lines
print(" ")


def destinations():
    #Here I used the inquirer module to ask the user for the travel destination
    choice = [
        inquirer.List(
            'destination',
            message="Please enter the travel destination",
            choices=['Auckland', 'Wellington',
                     'Rotorua']  #List of destinations
        ),
    ]
    class_type = inquirer.prompt(choice)
    print("Destination > " + class_type['destination'].upper()
          )  #Prints the chosen destination
    print(' ')


def discount_inputs(cue):
    #This loop ensures that input values are only positive integers
    while True:
        try:
            value = int(input(cue))
        except ValueError:
            print("Sorry, please enter a number.")
            continue

        if value < 0:
            print("Sorry, your input can't be negative.")
            continue
        else:
            break
    return value


def discount_types():
    #I used the inquirer module to ask the user for discount type and confirmation
    choice = [
        inquirer.List(
            'class',
            message="Enter the discount type",
            choices=['Economy Class', 'Business Class', 'First Class'],
        ),
    ]
    class_type = inquirer.prompt(choice)
    print("Discount Type > " + class_type['class'].upper())

    #Confirmation, yes will continue program no will end it
    confirmation = [
        inquirer.Confirm('continue', message="Are you sure?"),
    ]
    x = inquirer.prompt(confirmation)
    print(" ")

#Calling functions
destinations()
discount_types()

#Variables to ask the user for input
fare = discount_inputs("Enter the fare discount > $")
percentage = discount_inputs("Enter the discount percentage > ")
