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
                color = self.terminal.blue
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
                    "Sorry, this program only works for customers flying the next day"
                )
                sys.exit()
            else:
                print('')
                return True


def Cabin_Class():
    cabin_classes = [
        inquirer.List(
            'class',
            message="Please enter class of which the discount will be applied",
            choices=[
                'Economy Class', 'Premium Economy', 'Business Class',
                'First Class'
            ],
        ),
    ]
    class_type = inquirer.prompt(cabin_classes,
                                 render=OtherListConsoleRender())

    if class_type['class'] == 'Economy Class':
        x = original_price * 1

    elif class_type['class'] == 'Premium Economy':
        x = original_price * 1.4

    elif class_type['class'] == 'Business Class':
        x = original_price * 1.6

    elif class_type['class'] == 'First Class':
        x = original_price * 2

    else:
        sys.exit()

    delay_print("The current flight fare to {} in {} is ${}".format(
        destination['destination'], class_type['class'], x))


def Discount():
    pass



Destinations()
original_price = click.prompt('Please enter the flight fare to {}'.format(
    destination['destination']),
                              type=int)
print('\n')
Cabin_Class()
