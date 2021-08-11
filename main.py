import inquirer
from inquirer.render.console import ConsoleRender
from inquirer.render.console._list import List
import random
import sys
import time


# Program title
txt = ("Waikato Air Email Text Generator")
x = txt.title()
print(x)
print("\n")

# This class adds color to the command line interface
class OtherColorList(List):
    def get_options(self):
        choices = self.question.choices

        for choice in choices:
            selected = choice == choices[self.current]

            if selected:
                color = self.terminal.yellow
                symbol = '>'
            else:
                color = self.terminal.normal
                symbol = ' '
            yield choice, symbol, color

class OtherListConsoleRender(ConsoleRender):
    def render_factory(self, question_type):
        if question_type != 'list':
            return super(ConsoleRender, self).render_factory(question_type)
        return OtherColorList


# Destination function
def destinations():
    # Here I used the inquirer module to ask the user for
    # the travel destination
    choice = [
        inquirer.List(
            'destination',
            message="Please enter the travel destination",
            choices=['Auckland', 'Wellington',
                     'Rotorua']  # List of destinations
        ),
    ]
    class_type = inquirer.prompt(choice, render=OtherListConsoleRender())
    print("Your destination is " +
          class_type['destination'].upper())  # Prints the chosen destination
    print(' ')


# Discounts inputs functions
def discount_inputs(prompt):
    # This loop ensures that the input values are only positive integers
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, please enter a number.\n")
            continue

        if value < 0:
            print("Sorry, your input can't be negative.\n")
            continue
        else:
            break
    return value


# Discount types function
def discount_types():
    # I used the inquirer module to ask the user for discount type
    choice = [
        inquirer.List(
            'class',
            message="Enter the discount type",
            choices=[
                'Economy Class', 'Premium Economy', 'Business Class',
                'First Class'
            ],  # List of plane cabin classes
        ),
    ]
    class_type = inquirer.prompt(choice, OtherListConsoleRender())

    # Asks the user to enter Y or N case insensitive
    # Return true if the answer is Y
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("You picked " + class_type['class'] +
                       " are you sure? [y/n]: ".lower())
    if answer == "y":
        print('\n')
        return True
    else:
        while True:
            answer = str(input('Would you like to start again? [y/n]: '))
            if answer in ('y', 'n'):
                break
            print("invalid input.")
        if answer == 'y':
            print('\n')
            discount_types()  # Calls this function to restart the program
        else:
            print("Ok, see you next time!")
            sys.exit()  # Exits the program


# This function will hold the text that will be printed 
def text():
    email_txt_1 = (" text ")
    vars = [email_txt_1]
    print(random.choice(vars))

destinations()
discount_types()


# Variables to ask the user for input
fare = discount_inputs("Please enter the fare discount > ")
percentage = discount_inputs("Please enter the discount percentage > ")
