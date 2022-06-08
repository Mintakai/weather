from tkinter import *
from tkinter.font import BOLD
import requests
import yaml
from yaml import SafeLoader

BUTTON_TEXT = "Get Data"
UNIT = "c"
LABEL_TEXT = "Weather in "

city = "Vantaa"

def formulate_error_response_string():
    label.configure(text=f"Please provide a valid city... {city} was not accepted!")

def load_api_key():
    with open('weatherapikey.yaml', 'r') as f:
        data = list(yaml.load_all(f, Loader=SafeLoader))
        return data[0]['key']

def get_city():
    global city
    city = main_entry.get()
    display_weather_data_on_label()

def get_weather_data_from_weatherapi():
    key = load_api_key()
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={key}&q={city}")
    try:
        return response.json()["current"]["temp_c"]
    except (KeyError):
        return False

def display_weather_data_on_label():
    weather_data = get_weather_data_from_weatherapi()
    formulate_error_response_string() if (not weather_data) else label.configure(text=f"{LABEL_TEXT}{city}: {weather_data}{UNIT}")

def update_weather():
    display_weather_data_on_label()
    main_window.after(3600000, update_weather)

main_window = Tk()
main_window.title("Weather")

main_button = Button(main_window, command=get_city, text="Get weather!")
main_button.pack()

main_entry = Entry(main_window)
main_entry.pack()

label = Label(main_window, text=LABEL_TEXT, font=("Segoe UI", 18, BOLD))
label.pack()

update_weather()

main_window.mainloop()