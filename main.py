# J.A.R.V.I.S A.I Speech Assistant
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pygame  # For music functionality

# Initialize pygame mixer
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Error initializing pygame mixer: {e}")

chatStr = ""

def chat(query):
    """Handles chat functionality using OpenAI."""
    global chatStr
    try:
        print(chatStr)
        openai.api_key = apikey
        chatStr += f"Sir: {query}\n Jarvis: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"]
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        say("Sorry, I encountered an error while processing your request.")
        print(f"Error in chat function: {e}")
        return "Error occurred in chat."

def ai(prompt):
    """Handles AI-based responses using OpenAI."""
    try:
        openai.api_key = apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        say("Sorry, I encountered an error while processing your AI request.")
        print(f"Error in ai function: {e}")

def say(text):
    """Uses the system's text-to-speech functionality."""
    try:
        os.system(f'say "{text}"')
    except Exception as e:
        print(f"Error in say function: {e}")

def takeCommand():
    """Listens to the user's voice command and converts it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            say("Sorry, there was an issue with the speech recognition service.")
            print(f"Speech recognition error: {e}")
            return "Speech recognition error."
        except Exception as e:
            say("An error occurred while taking your command.")
            print(f"Error in takeCommand function: {e}")
            return "Some error occurred."

def playMusic(song_name):
    """Plays the specified music file from the 'music' directory."""
    try:
        # Define the path to the music directory
        music_directory = os.path.join(os.getcwd(), "/Users/avaish/J.A.R.V.I.S/music")
        song_path = os.path.join("/Users/avaish/J.A.R.V.I.S/music", "/Users/avaish/J.A.R.V.I.S/music/back_in_black_intro.mp3")

        # Check if the file exists
        if not os.path.exists(song_path):
            raise FileNotFoundError(f"The file {song_name} does not exist in the 'music' directory.")

        # Load and play the music
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        say("Playing music, sir.")
    except FileNotFoundError as e:
        say("Sorry, the music file was not found.")
        print(f"File not found: {e}")
    except pygame.error as e:
        say("Sorry, I couldn't play the music.")
        print(f"Pygame error: {e}")
    except Exception as e:
        say("An unexpected error occurred while playing music.")
        print(f"Error in playMusic function: {e}")

def stopMusic():
    """Stops the currently playing music."""
    try:
        pygame.mixer.music.stop()
        say("Music stopped, sir.")
    except pygame.error as e:
        say("Sorry, I couldn't stop the music.")
        print(f"Pygame error: {e}")
    except Exception as e:
        say("An unexpected error occurred while stopping music.")
        print(f"Error in stopMusic function: {e}")

def cleanup():
    """Stops the music and performs cleanup before exiting."""
    try:
        pygame.mixer.music.stop()  # Stop any playing music
        pygame.mixer.quit()  # Quit the pygame mixer
        print("Cleanup completed. Exiting program.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def introduceYourself():
    """Introduces J.A.R.V.I.S. to the user."""
    try:
        introduction = (
            "Greetings. I am J.A.R.V.I.S., Just A Rather Very Intelligent System – "
            "your personal AI assistant, designed to simplify tasks, answer queries, "
            "and keep you ahead of the curve. How may I assist you today, Sir?"
        )
        say(introduction)
        print(introduction)
    except Exception as e:
        say("Sorry, I encountered an error while introducing myself.")
        print(f"Error in introduceYourself function: {e}")

if __name__ == '__main__':
    try:
        print('Welcome to Jarvis A.I')
        say("Hello Sir, I am Jarvis. How can I help you today?")
        while True:
            query = takeCommand()
            # Handle commands
            if "play music" in query.lower():
                playMusic("back_in_black_intro.mp3")

            elif "stop music" in query.lower():
                stopMusic()

            elif "introduce yourself" in query.lower():
                introduceYourself()

            elif "the time" in query:
                try:
                    hour = datetime.datetime.now().strftime("%H")
                    minute = datetime.datetime.now().strftime("%M")
                    say(f"Sir, the time is {hour} hours and {minute} minutes.")
                except Exception as e:
                    say("Sorry, I couldn't fetch the time.")
                    print(f"Error fetching time: {e}")

            elif "open facetime" in query.lower():
                try:
                    os.system("open /System/Applications/FaceTime.app")
                except Exception as e:
                    say("Sorry, I couldn't open FaceTime.")
                    print(f"Error opening FaceTime: {e}")

            elif "open pass" in query.lower():
                try:
                    os.system("open /Applications/Passky.app")
                except Exception as e:
                    say("Sorry, I couldn't open Passky.")
                    print(f"Error opening Passky: {e}")

            elif "using artificial intelligence" in query.lower():
                ai(prompt=query)

            elif "jarvis quit" in query.lower():
                say("Goodbye, Sir.")
                cleanup()
                exit()

            elif "reset chat" in query.lower():
                chatStr = ""
                say("Chat history has been reset.")

            else:
                print("Chatting...")
                chat(query)

    except KeyboardInterrupt:
        say("Goodbye, Sir.")
        cleanup()
        print("Exiting Jarvis A.I.")
    except Exception as e:
        say("An unexpected error occurred. Exiting now.")
        cleanup()
        print(f"Unexpected error in main loop: {e}")
