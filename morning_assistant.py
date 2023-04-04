import os
import tkinter as ttk
from tkinter import *
import webbrowser
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

state = 'initial'


# hyperlink class
class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action, link):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = (action, link)
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(ttk.CURRENT):
            if tag[:6] == "hyper-":
                func, link = self.links[tag]
                func(link)
                return


# UI
root = Tk()
root.title("Gang's Morning Assistant v2")
root.geometry("640x480+500+300")

frame = Frame(root)
frame.pack()

# scraping
current_time = datetime.now()
# url lists:
weather_url = "https://weather.com/weather/today/l/de8c78996a73470bbe53d7ea51b93a733ee74f0744de3cf7660665e506a33862"
world_news_url = "https://www.nbcnews.com/world"
politics_news_url = "https://www.nbcnews.com/politics"
us_news_url = "https://www.nbcnews.com/us-news"

# weather soup
res_weather = requests.get(weather_url)
res_weather.raise_for_status()
weather_soup = BeautifulSoup(res_weather.text, "lxml")

# world news soup
res_world_news = requests.get(world_news_url)
res_world_news.raise_for_status()
world_news_soup = BeautifulSoup(res_world_news.text, "lxml")

# politics news soup
res_politics_news = requests.get(politics_news_url)
res_politics_news.raise_for_status()
politics_news_soup = BeautifulSoup(res_politics_news.text, "lxml")

# us news soup
res_us_news = requests.get(us_news_url)
res_us_news.raise_for_status()
us_news_soup = BeautifulSoup(res_us_news.text, "lxml")


def click(links):
    webbrowser.open(links)


def scrape_weather():

    location = weather_soup.find("h1", attrs={"class": "CurrentConditions--location--1YWj_"}).get_text()
    weather = weather_soup.find("div", attrs={"class": "CurrentConditions--phraseValue--mZC_p"}).get_text()
    curr_temp = weather_soup.find("span", attrs={"class": "CurrentConditions--tempValue--MHmYY"}).get_text()
    high_low = weather_soup.find("div", attrs={"class": "CurrentConditions--tempHiLoValue--3T1DG"}).get_text()

    txt.insert(END, "[AI] : Today's Weather: \n")
    txt.insert(END, location + current_time.strftime('%Y-%m-%d %H:%M'))
    txt.insert(END, weather)
    txt.insert(END, "Current Temp: " + curr_temp)
    txt.insert(END, high_low)

    weather_info = (
        "Today's Weather:\n"
        f"{location} {current_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"{weather}\n"
        f"Current Temp: {curr_temp}\n"
        f"{high_low}\n"
    )
    return weather_info


def scrape_world_news():
    world_top = world_news_soup.find_all("div", attrs={"class": re.compile("^tease-card__info")})
    world_news_1 = world_top[0].a['href']
    world_news_2 = world_top[1].a['href']

    # Create a new HyperlinkManager instance
    hyperlink_manager = HyperlinkManager(txt)

    # Add a new hyperlink using the add method and passing in the click function as a callback
    tags1 = hyperlink_manager.add(click, world_news_1)
    tags2 = hyperlink_manager.add(click, world_news_2)

    txt.insert(END, "[AI] : NBC TOP World News: \n")
    txt.insert(END, world_top[0].span.get_text())
    txt.insert(END, "\nlink\n", tags1)
    txt.insert(END, world_top[1].span.get_text())
    txt.insert(END, "\nlink\n", tags2)

    world_news_info = (
        "\nNBC TOP World News:\n"
        f"{world_top[0].span.get_text()}\n"
        f"{world_top[1].span.get_text()}\n"
    )
    return world_news_info


def scrape_politics_news():

    politics_top = politics_news_soup.find_all("div", attrs={"class": re.compile("^tease-card__info")})
    politics_news_1 = politics_top[0].a['href']
    politics_news_2 = politics_top[1].a['href']

    # Create a new HyperlinkManager instance
    hyperlink_manager = HyperlinkManager(txt)

    # Add a new hyperlink using the add method and passing in the click function as a callback
    tags1 = hyperlink_manager.add(click, politics_news_1)
    tags2 = hyperlink_manager.add(click, politics_news_2)

    txt.insert(END, "[AI] : NBC TOP Politics News: \n")
    txt.insert(END, politics_top[0].span.get_text())
    txt.insert(END, "\nlink\n", tags1)
    txt.insert(END, politics_top[1].span.get_text())
    txt.insert(END, "\nlink\n", tags2)

    politics_news_info = (
        "\nNBC Top Politics News:\n"
        f"{politics_top[0].span.get_text()}\n"
        f"{politics_top[1].span.get_text()}\n"
    )
    return politics_news_info


def scrape_us_news():

    us_top = us_news_soup.find_all("div", attrs={"class": re.compile("^tease-card__info")})
    us_news_1 = us_top[0].a['href']
    us_news_2 = us_top[1].a['href']

    # Create a new HyperlinkManager instance
    hyperlink_manager = HyperlinkManager(txt)

    # Add a new hyperlink using the add method and passing in the click function as a callback
    tags1 = hyperlink_manager.add(click, us_news_1)
    tags2 = hyperlink_manager.add(click, us_news_2)

    txt.insert(END, "[AI] : NBC TOP Politics News: \n")
    txt.insert(END, us_top[0].span.get_text())
    txt.insert(END, "\nlink\n", tags1)
    txt.insert(END, us_top[1].span.get_text())
    txt.insert(END, "\nlink\n", tags2)

    us_news_info = (
        "\nNBC Top Politics News:\n"
        f"{us_top[0].span.get_text()}\n"
        f"{us_top[1].span.get_text()}\n"
    )
    return us_news_info


global background_listener


# listen, STT
def listen(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language='en-US')
        txt.insert(END, '\n[User]: ' + text + '\n')
        answer(text)  # call answer() function with recognized text
    except sr.UnknownValueError:
        txt.insert(END, '\nVoice recognition failed')
    except sr.RequestError as e:
        txt.insert(END, '\nRequest failed : {0}'.format(e))


# answering
def answer(input_text):
    global state
    answer_text = ''
    if state == 'initial':
        if 'hi' in input_text or 'hello' in input_text:
            answer_text = 'How are you doing today?'
            txt.insert(END, "[AI] : " + answer_text)
        elif 'weather' in input_text:
            answer_text = scrape_weather()
        elif 'news' in input_text:
            answer_text = 'What type of news would you like? Choose from politics, U.S. or world.'
            txt.insert(END, "[AI] : " + answer_text)
            state = 'news_prompt'
        elif 'thank you' in input_text:
            answer_text = 'You\'re welcome'
            txt.insert(END, "[AI] : " + answer_text)
        elif 'bye' in input_text:
            answer_text = 'See you next time'
            txt.insert(END, "[AI] : " + answer_text)
            root.after(1000, root.destroy)
        else:
            answer_text = 'I\'m still here, but Sorry, I don\'t understand.'
            txt.insert(END, "[AI] : " + answer_text)
    elif state == 'news_prompt':
        if 'US' in input_text:
            answer_text = scrape_us_news()
        elif 'politics' in input_text:
            answer_text = scrape_politics_news()
        elif 'world' in input_text:
            answer_text = scrape_world_news()
        else:
            answer_text = 'I\'m still here, but Sorry, I don\'t understand.'
            txt.insert(END, "[AI] : " + answer_text)
        state = 'initial'
    speak(answer_text)


# TTS
def speak(text):
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='en')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):  # remove voice.mp3 file everytime
        os.remove(file_name)


# GUI:
scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

txt = Text(frame, yscrollcommand=scrollbar.set)
txt.pack()

scrollbar.config(command=txt.yview)

frame_option = Frame(root, relief="solid", bd=1)
frame_option.pack(side="bottom")


r = sr.Recognizer()
m = sr.Microphone()


def start_assistant():
    speak('How may I help you?')
    txt.insert(END, "[AI] : How may I help you?")
    global background_listener
    background_listener = r.listen_in_background(m, listen)


btn_start = Button(frame_option, text="Start", command=start_assistant)
btn_start.pack(side="left")


root.mainloop()
while True:
    time.sleep(0.1)
