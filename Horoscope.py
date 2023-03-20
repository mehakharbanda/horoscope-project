# Vital modules for operation
from bs4 import BeautifulSoup
import pyttsx3
import time
import requests
import pandas as pd
from rich import print
import cv2
from datetime import datetime
from datetimerange import DateTimeRange

# Python script to convert the given image
# into a dotted text using opencv


def image(sign: str, mark: str or int = "[cyan]![/cyan]", spaces: str or int = '.'):
    # Read the image
    img = cv2.imread(sign, 0)

    # Apply median blur
    img = cv2.medianBlur(img, 5)

    # Apply MEAN thresholding to get refined edges
    image = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Convert the image into a compatible size
    # We will use 60 pixels wide image so that text
    # fits in the console

    # Preserve the ratio
    ratio = len(image)/len(image[0])
    # Assign new width and calculate new height
    new_width = 60
    new_height = int(ratio*new_width)
    # Resize the image
    image = cv2.resize(image, (new_height, new_width))

    # Iterate over the array and print the dark pixels
    # or we can use any other symbol too.
    for i in range(len(image)):
        for j in range(len(image[0])):
            print(mark if image[i, j] < 100 else spaces, end="")
        print()

# Todays horoscope for the zodiac sign


def horoscope(zodiac: str, info: str = ''):
    # URL of website from where horoscope will be read
    url = f'https://www.ganeshaspeaks.com/horoscopes/daily{info}-horoscope/{zodiac}'
    website = requests.get(url)

    # Parsing the html content
    soup = BeautifulSoup(website.content, 'html.parser')

    # Changing the voice
    engine.setProperty('voice', voices[0].id)

    # Title of horoscope
    printSay(fronttext='[yellow]', text=soup.find(
        'h1').text, endtext='[/yellow]')

    # Changing the voice again
    engine.setProperty('voice', voices[1].id)

    # Finding the horoscope content
    para = soup.find_all('p')
    for i in para:
        if i.get('id') == "horo_content":
            printSay(fronttext='[cyan]', text=i.text,
                     endtext='[/cyan]', end='\n\n')

    # Change the voice into original one
    engine.setProperty('voice', voices[0].id)


# Initialising pttsx3 and setting attributes of it
engine = pyttsx3.init()
engine.setProperty('speed', 80)
voices = engine.getProperty('voices')

# Voice print


def printSay(text, fronttext='', endtext='', end='\n', printing=True):
    if printing:
        print(f'{fronttext}{text}{endtext}', end=end)
    time.sleep(0.25)
    engine.say(text)
    engine.runAndWait()

# Display info related to the zodiac sign


def display_table(sign: str):
    # Changing the voice
    engine.setProperty('voice', voices[1].id)

    # Reading zodiac table from excel worksheet
    table = pd.read_excel('Zodiac Sign Table.xlsx')

    # Dropping 'Signs' column
    table = table.drop('Signs', axis=1)

    # Getting detail for particular zodiac sign from the table
    index = table[table['Zodiac Sign'] == sign.capitalize()].index
    info = table[table['Zodiac Sign'] == sign.capitalize()].to_dict()
    print()

    # Printing the gattered informations of the sign
    for i in table.columns:
        print(
            f'[yellow]{i}[/yellow] : [cyan]{info.get(i).get(index[0])}[/cyan]')
        printSay(
            f'{i} : {info.get(i).get(index[0])}', end='\n\n', printing=False)
    print()


if __name__ == '__main__':
    # Intro
    # Shri Ganesha doted art
    image('Ganesha.jpg', mark='[yellow]o[/yellow]', spaces=' ')
    print()

    # Greeting
    printSay(fronttext='-----* [red]',
             text='WELCOME TO GANESHA DAILY HOROSCOPE', endtext='[/red] *-----', end='\n\n')

    # Asking for DOB
    printSay("Enter your date-of-birth, here", printing=False)

    # Catching an error
    try:
        # Getting DOB into LIST type
        user_input = list(
            map(int, input("(dd-mm-yyyy) : ").split('-')))

        # Converting DOB list into TimeDelta Object
        dob = datetime(user_input[2], user_input[1], user_input[0])

        # Horoscope's topics
        zodiac_info = {0: '', 1: '-love-and-relationship', 2: '-health-and-well-being',
                       3: '-money-and-finance', 4: '-career-and-business'}

        # Making time range for each zodiac sign
        zodiac_dates = {'aries': DateTimeRange(datetime(user_input[2], 3, 21), datetime(user_input[2], 4, 20)), 'taurus': DateTimeRange(datetime(user_input[2], 4, 21), datetime(user_input[2], 5, 21)), 'gemini': DateTimeRange(datetime(user_input[2], 5, 22), datetime(user_input[2], 6, 21)), 'cancer': DateTimeRange(datetime(user_input[2], 6, 22), datetime(user_input[2], 7, 22)), 'leo': DateTimeRange(datetime(user_input[2], 7, 23), datetime(user_input[2], 8, 23)), 'virgo': DateTimeRange(datetime(user_input[2], 8, 24), datetime(user_input[2], 9, 22)), 'libra': DateTimeRange(
            datetime(user_input[2], 9, 23), datetime(user_input[2], 10, 23)), 'scorpio': DateTimeRange(datetime(user_input[2], 10, 24), datetime(user_input[2], 11, 22)), 'sagittarius': DateTimeRange(datetime(user_input[2], 11, 23), datetime(user_input[2], 12, 21)), 'capricorn': DateTimeRange(datetime(user_input[2], 12, 22), datetime(user_input[2]+1, 1, 20)), 'aquarius': DateTimeRange(datetime(user_input[2], 1, 21), datetime(user_input[2], 2, 18)), 'pisces': DateTimeRange(datetime(user_input[2], 2, 19), datetime(user_input[2], 3, 20))}

        # Checking DOB in each time range of zodiac sign
        for key, daterange in zodiac_dates.items():
            if dob in daterange:
                zodiac = key
                break

        # Zodiac Symbol
        image(f"signs\{zodiac}.jpg", spaces=' ')

        # Telling the user's zodiac sign according to DOB
        printSay(
            fronttext='[red]', text=f'OK ! Your zodiac sign is {zodiac}, according to your date-of-birth... Some astrological informations related to you are :', endtext='[/red]')

        # Getting info from the zodiac excel worksheet for a particular zodiac sign
        display_table(sign=zodiac)

        # Moving towards the horoscope
        printSay(fronttext='[red]', text='PREDICTIONS OF TODAY FOR YOU :',
                 endtext='[/red]', end='\n\n')

        # Reading horscope for each topic of the selected zodiac sign
        for i in zodiac_info.keys():
            horoscope(zodiac, zodiac_info.get(i))

    # Skipping errors and continuing the flow of program
    except Exception as e:
        pass

    # Outro
    printSay(
        fronttext='[red]', text='THANKS FOR USING... HAVE A NICE DAY !', endtext='[/red]')
    printSay(
        fronttext='[red]', text='FOR MORE INFO CONTACT HERE: 90XXX-XXXXX', endtext='[/red]')
