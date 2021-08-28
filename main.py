import sys
import time
import click
import random
import inquirer
from inquirer.render.console import ConsoleRender
from inquirer.render.console._list import List


def delay_print(string):
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)


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
    global discount
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
        answer = input("\n\nAre you sure? [y/n]: ")
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
                print(Colour.RED + "\nInvalid input!" + Colour.END)
        if answer == 'y':
            print('\n')
            Discount()
        else:
            print("Ok, see you next time!")
            sys.exit()


def Seats():
    seats = 168
    delay_print(Colour.BOLD +
                "The current seating capacity is {}\n\n".format(seats) +
                Colour.END)

    delay_print(Colour.BOLD + "".format() + Colour.END)


def Loading_Animation():
    pass


def Email():
    customer_name = click.prompt("\nPlease enter the customers first name\n",
                                 type=str)

    email_subject = delay_print("\n\nSubject:\n" +
                                "{}%! discount on Waikato Air {} flights".
                                format(discount, class_type['class']).title())

    email_text_1 = delay_print(
        "\n\nText:\n" + "Dear {},\n\n".format(customer_name.title()) +
        "Whether you're looking for the lowest price, the most amount of flexibility or \n"
        "extra benefits, waikato air has the best fares for you.\n\n"
        "We are currently introducing a {}% discount on all {} flights to {}.\n"
        "Book now while seats last!".format(discount, class_type['class'],
                                            destination['destination']))

    if destination['destination'] == 'Wellington':
        events = ("Te Papa mueseum to it's\n"
                  "hunderds of different restaraunts\n"
                  "and everything in between!")

    elif destination['destination'] == 'Auckland':
        events = ("events such as the Auckland Lantern Festival\n"
                  "to asb classic and activities such as the Sky Tower"
                  "bungee jump or the Auckland art gallery.\n")

    elif destination['destination'] == 'Rotorua':
        events = ("the Skyline luge cart and gondala to \n"
                  "Crankworx mountain biking compitition\n"
                  "Rotorua has a place for you!\n")

    else:
        sys.exit()

    email_text_2 = delay_print(
        "\n\nText:\n" + "Hi {},\n\n".format(customer_name.title()) +
        "{} has something for everyone from {}\n".format(
            destination['destination'], events) +
        "\nWaikato air is currently having a {}% off sale on all {} flights to {}.\n"
        "Book now while seats last!\n".format(discount, class_type['class'],
                                              destination['destination']))


Destinations()
original_price = click.prompt('Please enter the flight fare to {}'.format(
    destination['destination']),
                              prompt_suffix=": $",
                              type=int)
print('\n')
Cabin_Class()
Discount()
Seats()
Loading_Animation()
Email()
