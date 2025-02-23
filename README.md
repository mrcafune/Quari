
# 💬 Quari - Terminal AI Assistant
CLI ChatGPT Front End that utilizes the ChatGPT API

![Screenshot 2024-07-20 at 1 04 17 AM](https://github.com/user-attachments/assets/1f210794-7a87-4f1c-a039-866b0faabad3)

**Quari** is the successor to KittyChat, a CLI, API dependent frontend for ChatGPT.

**Quari** is an interactive Python application that integrates OpenAI's models to create a CLI conversation interface.

## 🔑 Key Features

- **Color-coded Dialogue:** Messages are color-coded for a more visual and intuitive user experience. 
- **Session Management:** Start a new conversation or continue from a saved session. The application can store your conversation history for later reference.
- **Command Options:** Use various commands for improved interactivity and control over the application by typing -help.

## 🖥️ Usage

To use Quari, you will need to have an API key from OpenAI. On first-time setup, you will be prompted for your API key and desired model.  You can also run a reset command anytime to enter a new key, etc.

After starting the application, you can choose to start a new conversation or load a previous session. The application will guide you with the available commands and options by entering `-help`. During the conversation, type your message after the "Message:" prompt, and the virtual assistant will respond accordingly.

## 👩‍💻 Commands

- `-exit`: Exit the conversation. You'll be prompted to save the conversation.
- `-alwaysask`: Always ask at startup whether to start a new conversation or load a previous one.
- `-neverask`: Never ask at startup, always start a new conversation.
- `-help`: Display the help message. (lol)
- `-model`: Change the AI Model.
- `-sessionsummary`: Prints the loaded session's previous conversation.
- `-reset`: Runs the first-time setup, allowing you to change the API key & model.
- `-clearscreen`: Clears the screen of all previous text.

## 🗺️ Roadmap 

- ✅ **[Complete]** Better Formatting of Responses  
Modify the response to be more readable and account for styles of information, like code and list.

- ✅ **[Complete]** Improved Session System  
Provide tools to print the entire previous session, parts of it, set one or the other by default on load, etc.

- ✅ **[Complete]** Create 'First Time Setup'  
Allow users to enter API keys on initial setup rather than manually setting it, and choose what model you want.

- ✅ **[Complete]** Improved Help  
Format the help command, add additional options for navigation.

- ⏳ **QA & Bugtesting 2025**
QA & Bugtest the current build.  Perhaps update the roadmap with any new features.

- ⏳ **Application Packagement**  
Deploy the finished application to Flatpak, Snap, Deb, and RPM.
