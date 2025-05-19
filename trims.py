import tkinter as tk
from tkinter import scrolledtext
import spacy
import weatherapi
import socket
import io
import sys

# spaCy laadimine
nlp = spacy.load("en_core_web_sm")

def capture_weather_output(city):
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    try:
        weatherapi.weather_data(city)
    finally:
        sys.stdout = old_stdout  # Taasta stdout
    
    return buffer.getvalue()

# Kontrolli internetiühendust
def internet_connection(host='8.8.8.8', port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Asukoha leidmine tekstist
def location_selection(doc):
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None

# Tekstianalüüs ja tulemus
def analyze_input():
    sentence = input_text.get("1.0", tk.END).strip()
    doc = nlp(sentence)

    if any(token.text.lower() == "weather" and token.pos_ == "NOUN" for token in doc):
        city = location_selection(doc)
        if not city:
            result = "Palun täpsusta linna nimi."
        else:
            result = capture_weather_output(city) 

    elif sentence.lower() == "help":
        result = "Käsklused: weather <linn>, help, exit"
    elif sentence.lower() == "exit":
        root.quit()
        return
    else:
        result = "Tundmatu käsk."

    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("T.R.I.M.S. GUI v1.6")

tk.Label(root, text="Sisesta käsk (nt: weather in Tallinn):").pack(pady=5)

input_text = scrolledtext.ScrolledText(root, height=3, wrap=tk.WORD)
input_text.pack(padx=10, pady=5)

tk.Button(root, text="Aktiveeri", command=analyze_input).pack(pady=5)

tk.Label(root, text="Tulemus:").pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, state='disabled')
output_text.pack(padx=100, pady=50)

# Interneti ühenduse kontroll
if not internet_connection():
    output_text.config(state='normal')
    output_text.insert(tk.END, "Internetiühendust ei tuvastatud. Mõned funktsioonid ei pruugi toimida.\n")
    output_text.config(state='disabled')

root.mainloop()
