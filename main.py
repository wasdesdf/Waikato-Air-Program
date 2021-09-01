import sys  # To exit the program and for it's write and flush functions.
import time  # For delay
import click  # For inputs
import random  # To pick a random function
import inquirer  # For inputs
import itertools
from threading import Thread
from itertools import cycle, islice  #  For infinite cycling through a list
from inquirer.render.console import ConsoleRender  # To customize inquirer inputs
from inquirer.render.console._list import List  # ------------------


# This function creates cool "animated" text
# by putting a delay between each character in a string.
def delay_print(string):
    for i in string:  # Does the following for each character in a string
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(
            0.05
        )  # Used to set the delay between the characters/sets the animation speed


# Here it is being used to print the program title.
delay_print("Waikato Air Email Text Generator\n\n\n".title())


# These classes are used to customize the inquirer inputs
class OtherColorList(List):
    def get_options(self):
        choices = self.question.choices

        for choice in choices:
            selected = choice == choices[self.current]

            if selected:
                color = self.terminal.cyan
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


# I had to create two seprate "remove line" functions
# because I couldn't figure out how to create one function
# for two different uses.

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def Remove_Cabin_Class_Lines(n=17):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def Remove_Discount_Lines(n=8):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def Destinations():
    global destination
    destination_choices = [
        inquirer.List('destination',
                      message="Please enter the travel destination",
                      choices=['Auckland', 'Wellington', 'Rotorua']),
    ]
    destination = inquirer.prompt(destination_choices,
                                  render=OtherListConsoleRender())


def Flight_Confirmation():
    while True:
        answer = input(
            "Can the customer fly tomorrow? [y/n]: ").strip().lower()
        if answer in ("y", "n"):
            if answer == "n":
                print(
                    "Sorry, this program only works for customers flying the next day."
                )
                sys.exit()
            else:
                print('')
                return True


def Original_Price():
    global original_price
    original_price = click.prompt(
        '\n\nPlease enter the flight fare to {}'.format(
            destination['destination']),
        prompt_suffix=": $",
        type=int)


def Cabin_Class():
    global class_type
    global discounted_fare
    cabin_classes = [
        inquirer.List(
            'class',
            message="Please enter the cabin class",
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

    confirmation_message = click.confirm("\n\nAre you sure", default=True)

    if confirmation_message == True:
        delay_print('\n')

    elif confirmation_message == False:
        confirm = click.confirm(
            "\nWould you like to enter the infomation again", default=True)
        if confirm == True:
            Remove_Cabin_Class_Lines()
            Original_Price()
            delay_print('\n')
            Cabin_Class()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Discount():
    global discounted_price
    global discount

    discount = click.prompt("\nPlease enter the discount percentage",
                            prompt_suffix=': %',
                            type=int)
    discounted_price = discounted_fare - (discounted_fare * discount / 100)

    if discounted_price < 0:
        delay_print(
            Colour.RED +
            "\nThe number you entered is too high!, please enter a lower discount.\n"
            + Colour.END)
        Discount()

    delay_print(Colour.BOLD +
                "\nThe discounted price to {} in {} is ${:.2f}".format(
                    destination['destination'], class_type['class'],
                    discounted_price) + Colour.END)

    confirmation_message = click.confirm("\n\nAre you sure", default=True)

    if confirmation_message == True:
        delay_print('\n')

    elif confirmation_message == False:
        confirm = click.confirm(
            "\nWould you like to enter the discount percentage again?",
            default=True)

        if confirm == True:
            Remove_Discount_Lines()
            Discount()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Seats():
    global seats
    seats = 168
    delay_print(Colour.BOLD +
                "\nThe current seating capacity is {}\n\n".format(seats) +
                Colour.END)


def Email():
    global customer_name
    global events
    customer_name = click.prompt("\nPlease enter the customers first name",
                                 type=str)

    email_subject = delay_print("\n\nSubject:\n" +
                                "{}%! discount on Waikato Air {} flights".
                                format(discount, class_type['class']).title())

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


def Cool_Loading_Animation(
):  # Not really waiting for anything to load, just here to look cool
    x = ["|", "/", "-", "\\"]  # This list is looped to create the animation
    for i in islice(cycle(x), 15 * len(x)):  # Loops through list 15 times
        sys.stdout.write('Generating Email ')
        print(i, end='\r')  # '\r' Clears the previous output
        time.sleep(0.1)  # Sleep function adds delay/sets animation speed


def Text_1():
    email_text_1 = delay_print(
        "\n\nText:\n" + "Dear {},\n\n".format(customer_name.title()) +
        "Whether you're looking for the lowest price, the most amount of flexibility or \n"
        "extra benefits, waikato air has the best fares for you.\n\n"
        "We are currently introducing a {}% discount on all {} flights to {}.\n"
        "Book now while seats last!".format(discount, class_type['class'],
                                            destination['destination']))


def Text_2():
    email_text_2 = delay_print(
        "\n\nText:\n" + "Hi {},\n\n".format(customer_name.title()) +
        "{} has something for everyone from {}\n".format(
            destination['destination'], events) +
        "Waikato air is currently having a {}% off sale on all {} flights to {}.\n"
        "Book now while seats last!\n".format(discount, class_type['class'],
                                              destination['destination']))


def Text_3():
    pass


def restart():
    restart = click.confirm('\n\nWould you like to generate another email?',
                            default=True)

    if restart == True:
        x = seats - 1
        Seats()
        Email()
    elif restart == False:
        delay_print("Ok, see you next time!\n")
        sys.exit()


# Calling functions
Destinations()

flight_confirmation = click.confirm("Can the customer fly tomorrow",
                                    default=True)

if flight_confirmation == True:
    Original_Price()
    delay_print('\n')
    Cabin_Class()
elif flight_confirmation == False:
    delay_print(
        "\nSorry, this program is only for users flying the next day.\n")
    sys.exit()

Discount()
Seats()
Email()

x = [Text_1, Text_2]
random.choice(x)()

restart()
