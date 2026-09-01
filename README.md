```markdown
# Terminal Gemini Chatbot

A lightweight, interactive command-line interface chatbot built with Python and the official Google GenAI SDK (`google-genai`). It features color-coded terminal outputs, a multi-threaded "Thinking..." spinner animation, and robust error handling with automatic rate-limit (429) and server-demand (503) retries.

## Features

* **Interactive CLI Chat**: Continuous conversation loop supporting clean exits (`exit`, `Ctrl+C`, `Ctrl+D`).
* **Visual Loading Feedback**: Multi-threaded spinner animation (`⠋⠙⠹...`) that runs while waiting for model responses.
* **ANSI Terminal Styling**: Color-coded output for readability (Green for User, Cyan for Gemini, Yellow for status/warnings, Red for errors).
* **Smart Error Recovery**: Automatically parses Google API rate-limit wait times via regex or applies exponential backoff for server overloads, sleeping the thread and retrying seamlessly.

## Prerequisites

* Python 3.10 or higher installed on your machine.
* A Google account to generate a free API key.

## Installation & Setup

### 1. Clone the Repository
Open your terminal and clone your repository from GitHub, then navigate into the project directory:
```bash
git clone https://github.com/dsunday05034-crypto/gemini-chatbot.git
cd the-repo-name

```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install google-genai python-dotenv

```

## Getting a Gemini API Key

To run this chatbot, you need a free or paid API key from Google AI Studio:

1. Navigate to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click on the **Get API key** button in the top left or center dashboard.
4. Click **Create API key in new project** (or select an existing project if prompted).
5. Copy your newly generated API key string. Keep it secure and do not share it publicly or push it to public repositories.

## Configuration

1. Create a file named `.env` in the root directory of your project folder:
```bash
touch .env

```


2. Open the `.env` file in your code editor and add your API key using this exact format:
```env
GEMINI_API_KEY=your_actual_api_key_here

```



## Running the Program

Execute the script from your terminal:

```bash
python main.py

```

Once running, type your message next to the green `You:` prompt and press **Enter**. To quit the chat session at any time, type `exit` or press `Ctrl + C`.

```

```