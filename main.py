def discount_inputs(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, please enter a number.")
            continue

        if value < 0:
            print("Sorry, your input can't be negative.")
            continue
        else:
            break
    return value


fare = discount_inputs("Enter the fare discount > ") 
percentage = discount_inputs("Enter the discount percentage > ")


def discount_types():
    message = ("Please enter the discount type.\n"
                "Enter 'e' for Economy, 'b' for Business, and 'f' for First.")

    types = {"e": "Economy", "b": "Business", "f": "First"}






