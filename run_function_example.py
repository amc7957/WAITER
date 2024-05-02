from process_order import process_order
from speech_to_text import speech_to_text

# User inputs order
print('Welcome! What would you like to eat? Our menu is below:')
print('1.) Steak\n2.) Burger\n3.) Chicken Sandwich')
sentence = input()

# Create menu
menu = [
    'number one',
    'number two',
    'number three',
    'burger',
    'steak',
    'chicken',
    'fry',
]


if __name__ =='__main__':

    order = sentence
    orderOutput, extrasOutput = process_order(order)
    print(orderOutput)
    print(extrasOutput)