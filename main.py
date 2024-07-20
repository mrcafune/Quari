import os
import sys
from openai import OpenAI
from colorama import Fore, Style, init
import json
import time
from datetime import datetime
import random
import threading

# Initialize colorama
init(autoreset=True)

# P neato, huh?  Make sure to set your API key as an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
conversation_log = [{"timestamp": current_datetime, "You": "Conversation started", "Kitten Technologies VA": ""}]

conversation_suggestions = {
    1: "Discuss the pros and cons of artificial intelligence.",
    2: "Explore the future of space exploration.",
    3: "Talk about the impact of climate change on global ecosystems.",
    4: "Analyze the themes of a famous novel.",
    5: "Debate whether time travel could ever be possible.",
    6: "Learn about different cultures and their traditions.",
    7: "Discuss the evolution of music through the decades.",
    8: "Explore theories about the origin of the universe.",
    9: "Talk about the rise of virtual reality.",
    10: "Discuss the ethical implications of gene editing.",
    11: "Explore the impact of social media on human communication.",
    12: "Discuss the life and impact of a historical figure.",
    13: "Talk about innovations in renewable energy.",
    14: "Explore the history and future of the Internet.",
    15: "Analyze the psychological effects of pandemic lockdowns.",
    16: "Discuss the art of filmmaking and its evolution.",
    17: "Talk about the future of artificial intelligence in healthcare.",
    18: "Explore the rise of eSports and gaming culture.",
    19: "Discuss the implications of universal basic income.",
    20: "Explore marine biology and the life of sea creatures.",
    21: "Discuss strategies for effective learning and education.",
    22: "Talk about advances in automobile technology.",
    23: "Explore the significance of major scientific discoveries.",
    24: "Discuss the importance of biodiversity and conservation efforts.",
    25: "Analyze different leadership styles and their effectiveness.",
    26: "Explore the mysteries of black holes and dark matter.",
    27: "Discuss the ethics of using drones in modern warfare.",
    28: "Talk about the history of human rights movements.",
    29: "Explore the psychology behind dreams and their meanings.",
    30: "Analyze the effects of globalization on economies.",
    31: "Discuss the potential for life on other planets.",
    32: "Talk about the role of AI in modern education.",
    33: "Explore the impact of cryptocurrencies on financial markets.",
    34: "Discuss the relevance of classical music today.",
    35: "Explore the world of haute couture and fashion design.",
    36: "Discuss the challenges of space colonization.",
    37: "Talk about the rise of digital art and NFTs.",
    38: "Explore the impact of AI on traditional jobs.",
    39: "Discuss the latest trends in science and technology.",
    40: "Explore the role of mental health awareness in society.",
    41: "Analyze the impact of advertising on consumer behavior.",
    42: "Discuss the future of biotechnology in medicine.",
    43: "Talk about the socio-economic impacts of climate change.",
    44: "Explore the evolution of human languages.",
    45: "Discuss the ethical boundaries of AI in personal lives.",
    46: "Explore the concept of sustainable urban planning.",
    47: "Discuss the influence of media on public opinion.",
    48: "Analyze the concept of quantum computing.",
    49: "Talk about the interplay between politics and media.",
    50: "Explore the future of human-computer interaction."
}

farewell_dict = {
    'English': 'Goodbye, you are loved',
    'Spanish': 'Adiós, eres amado',
    'French': 'Au revoir, tu es aimé',
    'German': 'Auf Wiedersehen, du wirst geliebt',
    'Italian': 'Addio, sei amato',
    'Portuguese': 'Adeus, você é amado',
    'Russian': 'Прощай, ты любим',
    'Chinese (Simplified)': '再见，你被爱着',
    'Japanese': 'さようなら、あなたは愛されています',
    'Korean': '안녕, 사랑받고 있어'
}

def random_farewell():
    # Randomly select a key from the dictionary
    language = random.choice(list(farewell_dict.keys()))
    # Print the phrase in the selected language
    print(f"{farewell_dict[language]}")
    print("")

def random_conversation_suggestion():
    suggestion_number = random.randint(1, 50)
    print(conversation_suggestions[suggestion_number])

def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        time.sleep(0.1)  # Feel free to experiment with the speed here
        sys.stdout.write("\r" + animation[idx % len(animation)])
        sys.stdout.flush()
        idx += 1
    sys.stdout.write("\r" + " " * len(animation) + "\r")  # Clear the animation
    sys.stdout.flush()

def print_conversation_from_json(filename="conversation_log.json"):
    try:
        with open(filename, "r") as file:
            conversation_list = json.load(file)
        
        print(f"Conversation loaded from {filename}:\n")
        for entry in conversation_list:
            user_entry = entry.get("user", "")
            ai_entry = entry.get("ai", "")
            print(f"You: {user_entry}")
            print(f"AI: {ai_entry}\n")
    
    except FileNotFoundError:
        print(f"No such file: {filename}")

# Saving / Loading conversations ----------------------------------------
def load_and_print_session(filename, session_name):

    print_conversation_from_json(f"{session_name}_c.json")

    if not os.path.isfile(filename):
        print("No saved session found.")
        return None
    else:
        with open(filename, 'r') as f:
            sessions = json.load(f)
        if session_name in sessions:
            session = sessions[session_name]
            print(f"\nSession name: {session_name}")
            for message in session:
                if message['role'] == 'system':
                    print(f"System: {message['content']}")
                elif message['role'] == 'user':
                    print(f"\033[94mYou: {message['content']}\033[0m")
                else:  # message['role'] == 'assistant'
                    print(f"\033[92mKitten Technologies Virtual Assistant: {message['content']}\033[0m")
        else:
            print("No session found with this name.")

# This is where we load / save our JSONs-----------------------------------
def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filename, data):
    print(Fore.YELLOW + "Data saved to file: " + Fore.WHITE)
    print(data)
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_config(filename):
    if not os.path.isfile(filename):
        config = {"first_time": True, "api_key": "", "model": ""}
        with open(filename, 'w') as f:
            json.dump(config, f)
        return config
    with open(filename, 'r') as f:
        try:
            config = json.load(f)
            # Just making sure that the model key is present
            if 'model' not in config:
                config['model'] = ""
            return config
        except json.JSONDecodeError:
            print("Failed to decode the configuration file.")
            return None
        
def save_config(filename, config):
    with open(filename, 'w') as f:
        json.dump(config, f)

# Goodbye words-------------------------------------------------------------
def clear_screen():
    if os.name == 'posix':  # for UNIX/Linux/MacOS
        _ = os.system('clear')
    else:  # for Windows
        _ = os.system('cls')

def save_conversation_to_json(conversation, filename="conversation_log.json"):
    with open(filename, "w") as file:
        json.dump(conversation, file, indent=4)

def choose_model():

    # Intro
    clear_screen()
    # Printing the title and version
    print(Fore.GREEN + "\nBeta Version" + Fore.WHITE + " Quari CLI Virtual Assistant")
    print(Fore.GREEN + "Last Updated " + Fore.WHITE + "June 2024")
    print(Fore.GREEN + "Version " + Fore.WHITE + "1.8\n")
    print("Welcome to " + Fore.CYAN + "Quari " + Fore.WHITE + "CLI Virtual Assistant")
    time.sleep(1)
    print("\n\nGenerating Configuration File...\n")
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()
    time.sleep(3)  # Simulate the time taken to generate the configuration file
    stop_event.set()
    loading_thread.join()
    print("")
    clear_screen()
    print(Fore.GREEN + "\nBeta Version" + Fore.WHITE + " Quari CLI Virtual Assistant")
    print(Fore.GREEN + "Last Updated " + Fore.WHITE + "June 2024")
    print(Fore.GREEN + "Version " + Fore.WHITE + "1.8\n")
    print("Welcome to " + Fore.CYAN + "Quari " + Fore.WHITE + "CLI Virtual Assistant")
    print(Fore.GREEN + "\n\nSuccess!" + Fore.WHITE + " Generated config.json\n")
    print(Fore.WHITE + "Press Enter to Continue")
    input()

    clear_screen()
    print(Fore.GREEN + "Please select your Model | Available Models:")
    print(Fore.WHITE + " ")
    print("(1) Model: gpt-4o\n")
    print("(2) Model: ggpt-4-turbo\n")
    print("(3) gpt-3.5-turbo\n")

    user_choice = input(Fore.YELLOW + "Enter the corresponding number for the model (without parentheses): " + Fore.WHITE)
    print(Fore.WHITE + " ")

    if user_choice == "1":
        return 'gpt-4o'
    elif user_choice == "2":
        return 'gpt-4-turbo'
    elif user_choice == "3":
        return 'gpt-3.5-turbo'
    else:
        print("Invalid choice. Defaulting to 'gpt-4o.")
        return 'gpt-4o'


def chat_with_openai(prompt):
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()
    response = client.chat.completions.create(model=chat_model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])
    stop_event.set()
    loading_thread.join()
    return response.choices[0].message.content.strip()

def format_response(response):
    formatted_response = ""
    inside_bold = False
    i = 0
    while i < len(response):
        if response[i:i+5] == '#####':
            formatted_response += Fore.BLUE + '#####'
            i += 5
            while i < len(response) and response[i] != '\n':
                formatted_response += response[i]
                i += 1
            formatted_response += Fore.RESET
        elif response[i:i+3] == '###':
            formatted_response += Fore.BLUE + '###'
            i += 3
            while i < len(response) and response[i] != '\n':
                formatted_response += response[i]
                i += 1
            formatted_response += Fore.RESET
        elif response[i] == '*' and not inside_bold:
            formatted_response += Fore.BLUE
            inside_bold = True
        elif response[i] == '*' and inside_bold:
            formatted_response += Fore.RESET
            inside_bold = False
        else:
            formatted_response += response[i]
        i += 1
    return formatted_response

c_model = " "

# Loading the configuration---------------------------------------------------

# Also loading the previous sessions
config_filename = 'config.json'
config = load_config(config_filename)
session_filename = 'saved_sessions.json'
saved_sessions = load_json(session_filename)

alwaysask = config.get('alwaysask', False)
neverask = config.get('neverask', False)
conversation = []

conversationSelected = False

while alwaysask or (not neverask and saved_sessions):
    action = input("Do you want to start a new session (N) or continue a previous session (P)? ")
    if action.lower() == 'p':
        print("Previous sessions:")
        for name in saved_sessions:
            print(name)
        session_name = input("Enter the name of the session you want to continue: ")
        conversation = saved_sessions.get(session_name, [])
        conversationSelected = True
        break
    elif action.lower() == 'n':
        conversationSelected = False
        break

config = load_config(config_filename)
if config is None:
    print("Unable to access or parse the config file.")
    print("Please check your permissions to the file.  Exiting program")
    exit()
elif "first_time" in config and not config["first_time"]:
    c_model = config["model"]
    clear_screen()
    if conversationSelected:
        print("Session loaded.")
    print("Config file loaded.")
    time.sleep(1)
    clear_screen()
else:
    config["first_time"] = False
    config["model"] = choose_model()
    save_config(config_filename, config)
    c_model = config["model"]
    print("Configuration Saved!")
    print("Press Enter to continue")
    input()
    clear_screen()

chat_model = c_model
# Here's the program baby------------------------------------------------------
def main():
    global conversation_log
    print(f"Initialized conversation_log: {conversation_log}")
    clear_screen()
    # Printing the title and version
    print(Fore.GREEN + "Developed by" + Fore.WHITE + " Kitten Technologies")
    print(Fore.GREEN + "Current Model " + Fore.WHITE + chat_model)
    print(Fore.GREEN + "Version " + Fore.WHITE + "2.0")
    print("Type " + Fore.YELLOW + "-help" + Fore.WHITE + " for additional commands")
    time.sleep(1)
    # purple = Fore.MAGENTA
    # light_blue = Fore.CYAN

    green = Fore.GREEN
    light_blue = Fore.CYAN

    logo_lines = [
    "   _____             _ ",
    "  |     |_ _ ___ ___|_|",
    "  |  |  | | | .'|  _| |",
    "  |__  _|___|__,|_| |_|",
    "      |__|             "]

    # Activate purple & light blue
    """ colored_logo = [
    purple + logo_lines[0],
    Fore.LIGHTMAGENTA_EX + logo_lines[1],
    Fore.LIGHTCYAN_EX + logo_lines[2],
    Fore.LIGHTBLUE_EX + logo_lines[3],
    light_blue + logo_lines[4]]

    for line in colored_logo:
        print(line + Style.RESET_ALL) """
    
    # Activate green & light blue
    colored_logo = [
        green + logo_lines[0],
        Fore.LIGHTGREEN_EX + logo_lines[1],
        Fore.LIGHTCYAN_EX + logo_lines[2],
        Fore.LIGHTBLUE_EX + logo_lines[3],
        light_blue + logo_lines[4]
    ]

    # Printing the logo in logo_lines
    for line in colored_logo:
        print(line + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + "\nQuari CLI Virtual Assistant\n")
    time.sleep(1)

    # End of title and version
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation_log = [{"timestamp": current_datetime, "You": "Conversation started", "Kitten Technologies VA": ""}]

    # This is the chat loop
    while True:
        user_input = input(Fore.LIGHTCYAN_EX + "You: " + '\033[0m')
        conversation_log.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "You": user_input, "Kitten Technologies VA": ""})
        print("")
        print('\033[92m' + Fore.LIGHTMAGENTA_EX + 'Quari: ' + '\033[0m')
  
        # These are the chat options
        print(Fore.WHITE)
        if user_input.lower() == '-exit':
            if input("Do you want to save this conversation (Y/N)? ").lower() == 'y':
                session_name = input("Enter a name for this session: ")
                saved_sessions[session_name] = conversation_log
                
                save_json(session_filename, saved_sessions)
                save_conversation_to_json(conversation_log, f"{session_name}_c.json")
                print("")
                random_farewell()
                break
            else:
                print("")
                random_farewell()
                break

        elif user_input.lower() == '-alwaysask':
            config['alwaysask'] = True
            config['neverask'] = False
            print("Configuration Changed: -alwaysask" + Fore.GREEN," [ON]" + Fore.WHITE, "")
            print("Configuration Changed: -neverask" + Fore.RED," [OFF]")
            save_json(config_filename, config)
            continue

        elif user_input.lower() == '-clearscreen':
            clear_screen()
            continue

        elif user_input.lower() == '-neverask':
            config['alwaysask'] = False
            config['neverask'] = True
            print("Configuration Changed: -neverask" + Fore.GREEN," [ON]" + Fore.WHITE, "")
            print("Configuration Changed: -alwaysask" + Fore.RED," [OFF]")
            save_json(config_filename, config)
            continue

        elif user_input.lower() == '-reset':
            config["first_time"] = True
            save_config(config_filename, config)
            # playsound('aheal.wav') # Uncomment if sound functionality is desired
            print("Reset complete. Program restarting...")
            exit()

        elif user_input.lower() == '-help':
            print(Fore.YELLOW + "Available Commands")
            print(Fore.YELLOW + "\n-exit:" + Fore.WHITE +"             Exit the conversation. You'll be prompted to save the conversation")
            print(Fore.YELLOW + "-alwaysask:" + Fore.WHITE + "        Always ask at startup whether to start a new conversation or load a previous one")
            print(Fore.YELLOW + "-neverask:" + Fore.WHITE + "          Never ask at startup, always start a new conversation")
            print(Fore.YELLOW + "-clearscreen:" + Fore.WHITE + "       Clears the terminal of text")
            print(Fore.YELLOW + "-help:" + Fore.WHITE + "             Display this help message")
            print(Fore.YELLOW + "-changemodel:" + Fore.WHITE + "      Deletes config file and takes you back to the Model Selection Screen")
            print(Fore.YELLOW + "-sessionsummary:" + Fore.WHITE + "   Prints the previous sessions conversation")
            print(Fore.YELLOW + "-reset:" + Fore.WHITE + "            Clears your API Key, runs first time setup")
            print(Fore.YELLOW + "-suggestion:" + Fore.WHITE + "       Suggests conversation ideas with Quari/KittyChat")
            continue
        
        elif user_input.lower() == '-suggestion':
            random_conversation_suggestion()
            print(" ")
            continue

        elif user_input.lower() == '-changemodel':
            choose_model()
            continue

        elif user_input.lower() == '-sessionsummary':
            session_name = input(Fore.YELLOW + "Verify Session Name\n" + Fore.WHITE)
            if session_name is not None:
                load_and_print_session(session_filename, session_name)
            else:
                print("No session has been started yet.")
            continue

        elif user_input.lower()[0] == '-':
            print("Unrecognized command. Available commands are -exit, -alwaysask, -neverask, -help.\n")
            continue
        
        # This is where the magic happens (openAI responds)
        response = chat_with_openai(user_input)
        formatted_response = format_response(response)

        conversation_log[-1]["Kitten Technologies VA"] = response

        print(f"{formatted_response}\n")

if __name__ == "__main__":
    main()
