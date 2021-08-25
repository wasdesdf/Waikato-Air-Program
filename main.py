# Importing modules, I used the inqurer module to create the cool answer selector,
# sys to exit the program, random to pick a from a selection of different output text, 
# and python timezone for the date
import sys
import random
import time
import inquirer
from inquirer.render.console import ConsoleRender
from inquirer.render.console._list import List
from datetime import datetime
from pytz import timezone


# Program title
def delay_print(string):  # This function makes text print out cool
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(
            0.07)  # Used the time module to put a delay between chracters


delay_print("Waikato Air Email Text Generator\n\n")


# This class adds color to the command line interface
# I got this code from >> https://github.com/magmax/python-inquirer/issues/11
class OtherColorList(List):
    def get_options(self):
        choices = self.question.choices

        for choice in choices:
            selected = choice == choices[self.current]

            if selected:
                color = self.terminal.yellow
                symbol = '>'
            else:
                color = self.terminal.grey
                symbol = '|'
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
    fares = {"WLG": 90, "AKL": 83, "ROT": 50}
    delay_print("\033[1mThe current fare to " + class_type['destination'] +
                " is {}\033[0m\n\n".format(fares))  # Prints the chosen destination

    confirmation = [
        inquirer.Confirm('continue',
                    message="Can the customer fly tomorrow"),
    ]
    answers = inquirer.prompt(confirmation)

    answer = ""
    while answer not in ["y", "n", "Y", "N"]:
        answer = input()
    if answer == 'y':
        print('\n')
        return True
    else:
        while True:
            answer = str(
                input("Would you like to enter the infomation again? [y/n]: "))
            if answer in ('y', 'n', 'Y', 'N'):
                break
                print("invalid input.")
        if answer == 'y':
            print("Ok, see you next time!")
            sys.exit()


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
    class_type = inquirer.prompt(choice, render=OtherListConsoleRender())

    # Asks the user to confirm wether or not
    # they are sure they want to continue
    answer = ""
    while answer not in ["y", "n", "Y", "N"]:
        answer = input('\033[1m' + "You picked " +
                       class_type['class'].lower() +
                       ", are you sure? [y/n]: " + '\033[0m')
    if answer == 'y':
        print('\n')
        return True
    else:
        while True:
            answer = str(
                input("Would you like to enter the infomation again? [y/n]: "))
            if answer in ('y', 'n', 'Y', 'N'):
                break
                print("invalid input.")
        if answer == 'y':
            print('\n')
            discount_types()  # Calls this function to restart the program
        else:
            print("Ok, see you next time!")
            sys.exit()  # Exits the program


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


def confirm_choice():
    delay_print(
        '\n\033[1m' +
        "You entered ${} fare discount and {}% percentage discount.\033[0m\n\n"
        .format(fare, percentage))

    answer = ""
    while answer not in ["y", "n"]:
        answer = input("\nAre you sure, would you like to continue [y/n]: ")
    if answer == 'y':
        print('\n')
        return True
    else:
        while True:
            answer = str(
                input(
                    "\nWould you like to enter the infomation again? [y/n]: "))
            if answer in ('y', 'n'):
                break
            print("invalid input.")
        if answer == 'y':
            print('\n')
            questions()
        else:
            print("Ok, see you next time!")
            sys.exit()  # Exits the program


destinations()
discount_types()

delay_print("Please enter the discount fare and percentage below:\n\n")


# Function to ask the user for discount inputs
def questions():
    global fare  # I made these global variables so I could use them
    # to format the message in the confirm_discount_input_choice function
    global percentage

    fare = discount_inputs("Please enter the fare discount > ")
    print(' ')
    percentage = discount_inputs("Please enter the discount percentage > ")
    confirm_choice()


questions()
