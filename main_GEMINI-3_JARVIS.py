import speech_recognition as sr  
import webbrowser 
import pyttsx3  
import musicLibrary
import requests
import datetime
import os
import pyautogui
import psutil
import wikipedia
import pyjokes
import cv2
import speedtest
import ctypes
from openai import OpenAI
from deepface import DeepFace
import cv2
import pyautogui
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading 
# -------------------- GLOBAL VARS --------------------
gui_root = None
text_area = None
# -------------------- VOICE SETUP --------------------
def speak(text):
    if text_area:
        text_area.configure(state='normal')
        text_area.insert(tk.END, f"Jarvis: {text}\n")
        text_area.see(tk.END)
        text_area.configure(state='disabled')

    print(f"Jarvis says: {text}") 
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[0].id) 
    except:
        pass 
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# -------------------- OPENAI SETUP --------------------
def AiProcess(command):
    client = OpenAI(api_key="Your-API-Key") 

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short responses."},
                {"role": "user", "content": command}
            ]
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        print(f"OpenAI Error: {e}")

# -------------------- WEATHER SETUP --------------------
def get_weather(city):
    api_key = "Your-API-Key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    try:
        url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            temp = main["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees celsius with {desc}")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather.")


# -------------------- NEWS SETUP --------------------
newsAPI = "Your-API-Key".strip()

def get_news():
    speak("Fetching latest news...")
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "pk",
            "apiKey": newsAPI
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        r = requests.get(url, params=params, headers=headers)
        
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            
            if not articles:
                speak("No top headlines found for Pakistan right now.")
                return

            day = ["first", "second", "third", "fourth", "fifth"]
            for i, item in enumerate(articles[:5]):
                speak(f"Today's {day[i]} news is: {item['title']}")
            
            speak("That's all for now.")
        else:
            speak("Sorry, I could not fetch the news.")
            
    except Exception as e:
        speak("Connection error in news fetching.")
# -------------------- PROCESS COMMAND --------------------
def processCommand(c):
    c = c.lower()
    
    if text_area:
        text_area.configure(state='normal')
        text_area.insert(tk.END, f"User: {c}\n")
        text_area.see(tk.END)
        text_area.configure(state='disabled')

    print(f"Processing: {c}")
    
    # --------------- WEBSITES-----------
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("http://www.google.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("http://www.youtube.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("http://www.facebook.com")
    elif "open twitter" in c:
        speak("Opening Twitter")
        webbrowser.open("http://www.twitter.com")
    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("http://www.instagram.com")
    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("http://www.github.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("http://www.linkedin.com")
    elif "open chat gpt" in c:
        speak("Opening Chat G P T")
        webbrowser.open("https://chat.openai.com/")
    elif "open w3schools" in c:
        speak("Opening W3 Schools")
        webbrowser.open("https://www.w3schools.com/python/")
    elif "open gemini" in c:
        speak("Opening Google Gemini")
        webbrowser.open("https://gemini.google.com/")

    # ----- NEWS COMMAND -----

    elif "news" in c:
        get_news()

    # ----- MUSIC COMMAND -----
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
            speak(f"Playing {song}")
        else:
            speak("Song not found in library")

    # ----- TIME AND DATE COMMANDS -----
    elif "time" in c:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the time is {strTime}")

    elif "date" in c:
        strDate = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {strDate}")

    # ----- OPEN APPS COMMANDS -----
    elif "open calculator" in c:
        speak("Opening Calculator")
        os.system("calc")
    elif "open notepad" in c:
        speak("Opening Notepad")
        os.system("notepad") 
    elif "open paint" in c:
        speak("Opening Paint")
        os.system("mspaint")

    # ----- SYSTEM CONTROL COMMANDS -----
    elif "shutdown" in c:
        speak("Shutting down the system in 20 seconds. Please save your work.")
        os.system("shutdown /s /t 20") 
    elif "restart my PC" in c:
        speak("Restarting the system in 10 seconds.")
        os.system("shutdown /r /t 10")
    elif "cancel" in c:
        speak("Cancelling shutdown sequence.")
        os.system("shutdown /a")
    elif "sleep mode" in c:
        speak("Going to sleep mode. Good night sir.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    # ----- VOLUME CONTROL ----- 
    elif "volume up" in c:
        pyautogui.press("volumeup", presses=5) 
        speak("Volume increased")
    elif "volume down" in c:
        pyautogui.press("volumedown", presses=5)
        speak("Volume decreased")
    elif "mute" in c or "unmute" in c:
        pyautogui.press("volumemute")
        speak("Volume toggled")

    # ----- Write ----- 
    elif "write" in c:
        speak("What should I write sir?")
        try:
            with sr.Microphone() as source:
                print("Listening for text...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5)
            text_to_write = r.recognize_google(audio)
            speak("Writing now...")
            pyautogui.write(text_to_write)
        except Exception as e:
            speak("Sorry, I could not understand.")

    # ----- Max/Min -----
    elif "hide all" in c or "minimize" in c:
        speak("Minimizing all windows")
        pyautogui.hotkey('win', 'd')
    elif "show all" in c or "maximize" in c:
        speak("Restoring windows")
        pyautogui.hotkey('win', 'd')

        # ----- Lock PC -----
    elif "lock pc" in c or "lock system" in c:
        speak("Locking the system")
        ctypes.windll.user32.LockWorkStation()

    # ----- Switch WIN -----
    elif "switch window" in c:
        speak("Switching window")
        pyautogui.hotkey('alt', 'tab')

    # ----- Weather status -----
    elif "weather" in c:
        speak("Which city?")
        try:
            with sr.Microphone() as source:
                print("Listening for city name...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            city = r.recognize_google(audio)
            print(f"City heard: {city}")
            get_weather(city)
        except sr.WaitTimeoutError:
            speak("I didn't hear the city name.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand the city name.")
        except Exception as e:
            print(f"City Input Error: {e}")
            speak("Something went wrong.")

    # ----- BATTERY STATUS -----
    elif "battery in pc" in c:
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                speak("I cannot find a battery. Are you on a Desktop?")
            else:
                percent = battery.percent
                plugged = battery.power_plugged
                status = "charging" if plugged else "discharging"
                speak(f"Sir, the battery is at {percent} percent and currently {status}.")
        except Exception as e:
            speak("Error reading battery status.")

    # ----- Wikipedia -----
    elif "wikipedia" in c:
        speak("Searching Wikipedia...")
        c = c.replace("wikipedia", "")
        try:
            results = wikipedia.summary(c, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except:
            speak("No results found.")

    # ----- Internet Speed Test -----
    elif "internet speed" in c:
        speak("Checking internet speed. Please wait a moment...")
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1024 / 1024 
            upload_speed = st.upload() / 1024 / 1024
            speak(f"Download speed is {download_speed:.2f} Mbps")
            speak(f"Upload speed is {upload_speed:.2f} Mbps")
            print(f"Down: {download_speed:.2f} | Up: {upload_speed:.2f}")
        except Exception as e:
            speak("Could not test internet speed.")

    # ----- Screenshot -----
    elif "screenshot" in c:
        speak("Taking screenshot")
        im = pyautogui.screenshot()
        im.save("screenshot.png")
        speak("Screenshot saved")
        os.startfile("screenshot.png")

    # ----- Selfie -----
    elif "take selfie" in c or "open camera" in c:
        speak("Opening camera, smile please!")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("selfie.jpg", frame)
            speak("Photo clicked and saved.")
            os.startfile("selfie.jpg")
        else:
            speak("Error accessing camera.")
        cap.release()
        cv2.destroyAllWindows()

    # ----- Facial detection -----
    elif "scan my mood" in c:
        speak("Let me analyze your facial expressions, sir. Please look at the camera.")
        try:
                os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
                cap = cv2.VideoCapture(0)
                speak("Scanning...")
                ret, frame = cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    emotion = analysis['dominant_emotion']
                    print(f"Detected Mood: {emotion}")
                    if emotion == "happy":
                        speak("You look happy sir! Seeing you smile makes my circuits work better.")
                    elif emotion == "sad":
                        speak("You look a bit sad. Don't worry sir, tough times don't last.")
                    elif emotion == "angry":
                        speak("Sir, you look very angry. Should I play some relaxing music to calm you down?")
                    elif emotion == "fear":
                        speak("You look scared. Is there a ghost behind me?")
                    elif emotion == "surprise":
                        speak("You look surprised! Did I say something smart?")
                    elif emotion == "neutral":
                        speak("You look calm and composed. Ready for work, sir.")
                    else:
                        speak(f"I detect that you are feeling {emotion}.")
                else:
                    speak("I couldn't access the camera, sir.")
                cap.release()
                cv2.destroyAllWindows()
        except Exception as e:
                pass

    # ----- Jokes -----
    elif "joke" in c:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)          
            
        # OpenAI Response
    else:
        output = AiProcess(c)
        speak(output)

# -------------------- MAIN LOGIC (Threaded) --------------------
def start_jarvis_logic():
    global r
    speak("Initializing Jarvis...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if text_area:
            text_area.configure(state='normal')
            text_area.insert(tk.END, ">> ADJUSTING NOISE...\n")
            text_area.configure(state='disabled')
        r.adjust_for_ambient_noise(source, duration=1)
        if text_area:
            text_area.configure(state='normal')
            text_area.insert(tk.END, ">> SYSTEM READY.\n")
            text_area.configure(state='disabled')
    while True:
        print("Listening for 'Jarvis'...")
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes sir?")
                try:
                    with sr.Microphone() as source:
                        print("Jarvis Active... Speak command")
                        r.adjust_for_ambient_noise(source, duration=0.5) 
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    processCommand(command)
                except sr.WaitTimeoutError:
                    speak("I didn't hear any command.")
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
                except Exception as e:
                    print(f"Command Error: {e}")
        except Exception as e:
            pass

# -------------------- GUI SECTION --------------------
def start_thread():
    t = threading.Thread(target=start_jarvis_logic)
    t.daemon = True
    t.start()
def play_gif(label, frames, delay, frame_index=0):
    if not frames: return
    frame = frames[frame_index]
    label.configure(image=frame)
    frame_index = (frame_index + 1) % len(frames)
    gui_root.after(delay, play_gif, label, frames, delay, frame_index)
def main_gui():
    global gui_root, text_area
    gui_root = tk.Tk()
    gui_root.title("jarvis")
    gui_root.geometry("600x800")
    gui_root.configure(bg="black")
    gui_root.resizable(True, True)
    lbl_head = tk.Label(gui_root, text="Jarvis", bg="black", fg="#00ccff", font=("Impact", 24))
    lbl_head.pack(pady=10)
    gif_path = "jarvis.gif" 
    frames = []
    if os.path.exists(gif_path):
        file = Image.open(gif_path)
        try:
            while True:
                resized = file.copy().resize((1250, 310))
                frames.append(ImageTk.PhotoImage(resized))
                file.seek(len(frames)) 
        except EOFError:
            pass
        lbl_anim = tk.Label(gui_root, bg="black")
        lbl_anim.pack(pady=10, expand=True)
        play_gif(lbl_anim, frames, delay=50)
    btn = tk.Button(gui_root, text="ACTIVATE SYSTEM", command=start_thread,
                    bg="#00ccff", fg="black", font=("Arial", 12, "bold"),
                    width=20, height=2)
    btn.pack(pady=20)
    lbl_footer = tk.Label(gui_root, text="Developed by MUHAMMAD BIN NADEEM", 
                          bg="#1e1e1e", fg="grey", font=("Arial", 30))
    lbl_footer.pack(side=tk.BOTTOM, pady=5)
    gui_root.mainloop()
if __name__ == "__main__":
    main_gui()