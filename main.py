import sys
import time
import click
import inquirer
from inquirer.render.console import ConsoleRender
from inquirer.render.console._list import List


def delay_print(string):
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.07)


delay_print("Waikato Air Email Text Generator\n\n\n")


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
                symbol = ''
            yield choice, symbol, color


class OtherListConsoleRender(ConsoleRender):
    def render_factory(self, question_type):
        if question_type != 'list':
            return super(ConsoleRender, self).render_factory(question_type)
        return OtherColorList


class Colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def Destinations():
    global destination
    destination_choices = [
        inquirer.List('destination',
                      message="Please enter the travel destination",
                      choices=['Auckland', 'Wellington', 'Rotorua']),
    ]
    destination = inquirer.prompt(destination_choices,
                                  render=OtherListConsoleRender())


def Fares(prompt):
    while True:
        answer = input("\nCan the customer fly tomorrow? [y/n]: " +
                       Colour.END).strip().lower()
        if answer in ("y", "n"):
            if answer == "n":
                print(
                    "Sorry, this program only works for customers flying the next day."
                )
                sys.exit()
            else:
                print('')
                return True


def Cabin_Class():
    global class_type
    global discounted_fare
    cabin_classes = [
        inquirer.List(
            'class',
            message="Please the cabin class",
            choices=[
                'Economy Class', 'Premium Economy', 'Business Class',
                'First Class'
            ],
        ),
    ]
    class_type = inquirer.prompt(cabin_classes,
                                 render=OtherListConsoleRender())

    if class_type['class'] == 'Economy Class':
        discounted_fare = original_price * 1

    elif class_type['class'] == 'Premium Economy':
        discounted_fare = original_price * 1.4

    elif class_type['class'] == 'Business Class':
        discounted_fare = original_price * 1.6

    elif class_type['class'] == 'First Class':
        discounted_fare = original_price * 2

    else:
        sys.exit()

    delay_print("The flight fare to {} in {} is ${:.2f}".format(
        destination['destination'], class_type['class'], discounted_fare))

    while True:
        answer = input(Colour.BOLD +
                       "\n\nWould you like to continue? [y/n]: " +
                       Colour.END).strip().lower()
        if answer in ("y", "n"):
            if answer == "n":
                print("Ok, see you next time!")
                sys.exit()
            else:
                print('')
                return True


def Discount():
    global discounted_price
    discount = click.prompt("\nPlease enter the discount percentage",
                            prompt_suffix=': %',
                            type=int)
    discounted_price = discounted_fare - (discounted_fare * discount / 100)
    delay_print(Colour.BOLD +
                "\nThe discounted price to {} in {} is ${:.2f}".format(
                    destination['destination'], class_type['class'],
                    discounted_price) + Colour.END)

    answer = ""
    while answer not in ["y", "n"]:
        answer = input(Colour.BOLD + "\n\nAre you sure? [y/n]: " + Colour.END)
    if answer == 'y':
        print('\n')
        return True
    else:
        while True:
            answer = str(
                input(
                    Colour.BOLD +
                    "\nWould you like to enter the infomation again? [y/n]: " +
                    Colour.END))
            if answer in ('y', 'n', 'Y', 'N'):
                break
                print("invalid input.")
        if answer == 'y':
            print('\n')
            Discount()
        else:
            print("Ok, see you next time!")
            sys.exit()


def Seats():
    seats = (168)
    calc_const = 0.2

    for seat in seats:
        x = discounted_price + calc_const
        return seats

    delay_print(Colour.BOLD +
                "The current seating capacity is {}\n".format(seats) +
                Colour.END)

    delay_print(Colour.BOLD + "".format() + Colour.END)


Destinations()
original_price = click.prompt('Please enter the flight fare to {}'.format(
    destination['destination']),
                              prompt_suffix=": $",
                              type=int)
print('\n')
Cabin_Class()
Discount()
Seats()
