import weatherapi
import fmsystem
#import pythonpackages
#import calendarapi
import os
import sys
import spacy
#import speech_recognition as sr
import json
import socket


def internet_connection(host='8.8.8.8', port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("Internet Connection Established")
        return True
    except socket.error as ex:
        print(ex)
        print("Some features may be unavailable")
        return False


def main_command():
    while True:
        print("-" * 20)
        sentence = input("Enter something: ")

        # Analyze text
        doc = nlp(sentence)
        
        if any(token.text.lower() == "search" and token.pos_ == "VERB" for token in doc):
            fmsystem.file_amount()

        if any(token.text.lower() == "weather" and token.pos_ == "NOUN" for token in doc):
            city = location_selection(doc)
            weatherapi.weather_data(city)

        if sentence.lower() == 'exit':
            print("Exiting program.")
            sys.exit()
            
        if sentence.lower() == 'help':
            help()
        #if user_input.lower() == 'check packages': 
         #   outdated_packages()
        #if user_input.lower() == 'upgrade packages':
         #   pythonpackages.upgrade_packages()
        #if user_input.lower() == 'list events':
         #   calendarapi.list_events()
        #if user_input.lower() == 'create events':
         #   calendarapi.create_events()
        #if user_input.lower() == 'spchrec':
            #speechrecognition()


def location_selection(doc):
    # Try to extract a GPE (Geopolitical Entity, like cities or countries)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            #print(f"Detected city: {ent.text}")
            return ent.text  # Return the first GPE detected

    # If no city was found, ask the user to specify one
    city = input("Sorry, can you please specify a city: ")
    return city


def help():
    with open('help_module.json', 'r') as file:
        data = json.load(file)
    input = data["commands"]
    print("-" * 30)
    for command, details in input.items():
        print(f"{details['text'].ljust(20)}{details['description']}")
    print("-" * 30)


def help_commands():
    with open('help_module.json', 'r') as file:
        data = json.load(file)
    helpinput = data["help-commands"]
    for command, details in helpinput.items():
        print(f"{details['description']}")


#def speechrecognition():
 #   recognition = sr.Recognizer()
  #  with sr.Microphone() as source:
   #     print("Please wait. Calibrating microphone...")
        # Listen for 1 second and create the ambient noise energy level
    #    recognition.adjust_for_ambient_noise(source, duration=1)
     #   print("Microphone calibrated. Say something!")

        # Capture the audio from the microphone
#        audio = recognition.listen(source)

 #       try:
            # Recognize speech using Google Web Speech API
  #          print("Recognizing...")
   #         text = recognition.recognize_google(audio)
    #        print("You said: " + text)
     #   except sr.RequestError:
      #      print("Could not request results from the speech recognition service.")
       # except sr.UnknownValueError:
        #    print("Could not understand the audio.")


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    print("Welcome to T.R.I.M.S. - Your Personal Virtual Companion - Version 1.6.11") # only change version if needed
    internet_connection()
    main_command()