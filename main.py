from urllib.request import urlopen
import speech_recognition as sr
from googlesearch import search
from pygame import mixer
import wolframalpha
import webbrowser
import wikipedia
import datetime
import requests
import pyjokes
import smtplib
import pyttsx3
import random
import json
import os

email = 'dtu.vishalsengar@gmail.com'
pw = 'DTU#2k18'

emailIDs = {"yogesh": "yk824422@gmail.com",
            "vishal": "vishalsengardtu@gmail.com",
            "kirti": "kirti.dn95@gmail.com"}


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 190)
engine.setProperty('volume', 1)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing...')
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")

    except Exception as err:
        print(err)
        print("Say that again please...")
        return "None"
    return command


def greetings():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    ass_name = 'Jarvis 2 point o'
    speak(f'I am your assistant {ass_name}')


def usrname():
    speak("What should i call you sir")
    uname = take_command()
    uname = uname.split(' ')[-1]
    speak(f"Welcome Mister {uname}")
    speak("How can i Help you.")


def how_are_you():
    li = ['good', 'great', 'fine']
    speak(f"I am {random.choice(li)}. and hope you are also {random.choice(li)} Sir")


def tasks():
    li_commands = [
        "open websites : Example: open youtube.com",
        "time : what time it is?",
        "day : what day is today?",
        "launch applications : launch chrome",
        "wikipedia search: Example: Wikipedia search India",
        "google search: Example: google search Ronaldo",
        "weather : Example: what is the weather/temperature in Mumbai?",
        "play a song : play a song",
        "send email : send email to vishal",
        "joke : tell a joke",
        "calculate : calculate 10 plus 14",
        "take a note: command",
        "where is : where is Delhi",
        "news: show some latest news",
    ]
    ans = """Sir, I can do lots of things, for example I can tell you day, time, weather in your city, I can open websites for you, I can launch desktop application, play songs, wikipedia searches, google searches, I can Find locations on map, I can perform basic arithmetic calculations, I can take down important notes, send emails, show latest news, I can even tell you funny jokes. See the list of commands-"""
    for i in li_commands:
        print(i)
    speak(ans)


def news():
    obj = urlopen('''https://newsapi.org/v2/top-headlines?country=in&apiKey=c2000743ab5a43719c0d8e47d34ec751''')
    data = json.load(obj)
    i = 1
    speak('here are some latest news from NEWSAPI.ORG')
    print('''=============== NEWSAPI.ORG ============''' + '\n')
    for item in data['articles']:
        print(str(i) + '. ' + item['title'] + '\n')
        print(item['description'] + '\n')
        speak(str(i) + '. ' + item['title'] + '\n')
        i += 1


def wikipedia_search():
    speak('What should I search for ?')
    topic = take_command()
    speak('Searching Wikipedia...')
    results = wikipedia.summary(topic, sentences=1)
    speak('According to wikipedia')
    print(results)
    speak(results)


def open_url(url):
    print(f'Opening {url}')
    speak(f'Opening {url}')
    webbrowser.register(
        'chrome', None,
        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(url)


def day():
    week_day = datetime.datetime.today().weekday() + 1
    day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
    day_of_the_week = day_dict[week_day]
    speak("Today is " + day_of_the_week)


def calculate(cmd):
    app_id = "3TJXH6-JH55TW8JR6"
    client = wolframalpha.Client(app_id)
    indx = cmd.lower().split().index('calculate')
    cmd = cmd.split()[indx + 1:]
    res = client.query(' '.join(cmd))
    answer = next(res.results).text
    print("The answer is " + answer)
    speak("The answer is " + answer)


def locate(location):
    speak(f"User asked to Locate {location}")
    webbrowser.open("https://www.google.co.in/maps/place/" + location + "")


def take_note():
    speak("Sir, what should i write?")
    note = take_command()
    file = open('jarvis.txt', 'w')
    speak("Sir, Should i include date and time")
    ans = take_command()
    if 'yes' in ans or 'sure' in ans:
        x = str(datetime.datetime.now())
        file.write(x)
        file.write(" :- ")
        file.write(note)
    else:
        file.write(note)
    speak('The notes are saved')


def show_note():
    speak("Showing latest Notes")
    file = open("jarvis.txt", "r")
    print(file.read())


def send_email(to, content):
    server = smtplib.SMTP('Smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, pw)
    server.sendmail(email, to, content)
    server.close()


def temp(city_name):
    api_key = "09e6e77a05755a7a29ce1cc9b2fd75cd"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        temperature = y["temp"] - 273.15
        humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        description = {f"Current temperature in {city_name} is {round(temperature, 1)} degree celsius, "
                       f"And the humidity level is {humidity} percent,  "
                       f"Overall the weather is {weather_description}"}
        return description


def search_on_google(query, output_list):
   speak("The top five search results from Google are listed below.")
   for output in search(query):
      print(output)
      output_list.append(output)
   return output_list


def open_link(output_list):
   speak("Here’s the first link for you.")
   webbrowser.open(output_list[0])


if __name__ == '__main__':
    greetings()
    usrname()

    while True:
        query = take_command().lower()

        # logic for executing tasks based on query
        if 'how are you' in query:
            how_are_you()

        elif 'what can you do' in query:
            tasks()

        elif 'news' in query:
            try:
                news()
            except Exception as e:
                speak('Sir, These were some of the latest news updates')

        elif 'wikipedia search' in query:
            wikipedia_search()

        elif 'open' in query:
            domain = query.split(' ')[-1]
            open_url(domain)

        elif "play music" in query or "play a song" in query:
            try:
                music_folder = "C:\\Users\\lahsi\\Music\\"
                music = os.listdir(music_folder)
                random_music = music_folder + random.choice(music)
                mixer.init()
                mixer.music.load(random_music)
                speak("Here’s your music, Enjoy !")
                mixer.music.play()
            except Exception as e:
                print(e)
                speak("I am sorry. Unable to play song at the moment")

        elif "stop the music" in query or "stop the song" in query or "stop" in query:
            mixer.music.stop()
            speak("The music is stopped.")

        elif 'time' in query:
            strTime: str = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "what day is today" in query or "what's the day today" in query:
            day()

        elif "calculate" in query:
            calculate(query)

        elif "where is" in query:
            place = query.replace("where is", "")
            locate(place)

        elif "write a note" in query or 'take a note' in query:
            take_note()

        elif "show note" in query:
            show_note()

        elif 'weather' in query:
            try:
                speak("Which city's weather report you want to know Sir? ")
                city = take_command()
                desc = temp(city)
                speak(desc)
            except Exception as e:
                print(e)
                speak("I am sorry. Unable to fetch the weather report at the moment")

        elif 'launch vs code' in query:
            codePath = 'C:\\Users\\lahsi\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe'
            os.startfile(codePath)

        elif 'google search' in query:
            outputList = []
            speak('Sir What should I search for ?')
            query = take_command()
            search_on_google(query, outputList)
            speak('Sir Should I open up the first link for you ?')
            query = take_command()
            if 'yes' in query or 'sure' in query:
                open_link(outputList)
            if 'no' in query:
                speak('Alright.')

        elif 'send email' in query:
            try:
                to = query.split(' ')[-1].lower()
                recipient = emailIDs[to]
                speak("Sir What should I send?")
                content = take_command()
                send_email(recipient, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("I am sorry, Unable to send this email at the moment.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'presentation' in query or 'PPT' in query:
            try:
                pptPath = 'C:\\Users\\lahsi\\OneDrive\\Desktop\\Virtual-Assistant.pptx'
                os.startfile(pptPath)
                speak("Opening the AI-Virtual Assistant Presentation")
            except Exception as e:
                print(e)
                speak("Unable to launch the presentation at the moment.")

        elif 'shutdown' in query:
            speak('Shutting down Jarvis 2 point o!. It was nice assisting you Sir.')
            exit()
