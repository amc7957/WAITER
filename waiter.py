import PySimpleGUI as sg
import time
import re
import speech_recognition as sr
from speech_recognition.recognizers import google, whisper
import pyttsx3 
from process_order import process_order

menu = ["steak","hamburger","burger","cheeseburger","chicken","number one","number 1","number two","number 2","number three","number 3"]

def text_to_speech(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    # use sr recognizer 
    r = sr.Recognizer() 

    while(1):    
        try:
        # initialize microphone
            with sr.Microphone() as source2:
                # wait for ambient noise level to be adjusted
                r.adjust_for_ambient_noise(source2, duration=0.2)
             
                # listen for speech
                audio2 = r.listen(source2)
             
                # use google recognizer to figure out what
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                return(MyText)
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            break 
        except sr.UnknownValueError:
            print("unknown error occurred")
            break


def main():
    sg.theme('DarkBlue3')
    sg.set_options(element_padding=(10, 10))
    # Define the layout for the menu
    layout = [
        [sg.Text('Click "Order" when you are ready to order', justification='center')],
        [sg.Text('1. Steak', justification='center')],
        [sg.Text('2. Hamburger', justification='center')],
        [sg.Text('3. Chicken', justification='center')],
        [sg.Text('', key = 'confirmation')], #empty space for order confirmation
        [sg.Button('Order', size=(20, 1))],
        [sg.Button('Exit', size=(20, 1))]
    ]

    # Create the PySimpleGUI window
    window = sg.Window('Menu', layout, element_justification='c')

    # Event loop
    while True:
        event, _ = window.read()

        # Exit if the user closes the window or clicks the "Exit" button
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        elif event == 'Order':
            #window['Record'].update('Recording...')
            text_to_speech("Welcome to our restaurant. What would you like to order?")
            customer_order = speech_to_text()
            print("You said: ", customer_order)

            parsed_order, orderTree = process_order(customer_order, menu)

            if len(parsed_order)==1:
                waiter_response = "You would like {}, is that right?".format(parsed_order[0])
            elif len(parsed_order)==2:
                waiter_response = "You would like {} and {} is that right?".format(parsed_order[0], parsed_order[1])
            elif len(parsed_order)==3:
                waiter_response = "You would like {},{}, and {}, is that right?".format(parsed_order[0], parsed_order[1], parsed_order[2])
            else:
                waiter_response = "I'm sorry, we don't have that. Please try ordering again"

            print("W.A.I.T.E.R: ",waiter_response)
            text_to_speech(str(waiter_response))

            #Clean up order list to display
            order_confirmation = str(parsed_order)

            regex = re.compile('[^a-zA-Z]')
            order_confirmation = regex.sub(' ', order_confirmation)
            display_order =  "Your order: " + order_confirmation

            window['confirmation'].update(display_order)


            window['Order'].update('Order Again')

            orderTree.draw()

        
    # Close the window when the loop exits
    window.close()

main()