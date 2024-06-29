# Animated-Spoon

## Content Moderation Bot 

___This Telegram bot is designed for automated monitoring and filtering of messages in chats to detect offensive language. It utilizes aiogram libraries for interacting with the Telegram API, redis for data storage, and httpx for HTTP requests to the Google Perspective API and OpenAI API. The bot checks each incoming message for length and validity, then analyzes the text for offensive words. If detected, the message can be deleted or modified. Additionally, the bot uses AI to replace offensive language with neutral equivalents while preserving the message's meaning and structure. All errors are logged and sent to the administrator for further analysis and correction.___


## Here's a detailed breakdown of how the bot works:

__Initialization and Setup:__
1. Libraries and APIs:
    >The bot uses 'aiogram' library to interact with the Telegram API.
    
    > 'redis' is utilized for data storage.

    > 'httpx' is used for making HTTP requests.

2. APIs and API Tokens:
    > 'OPENAI_API_TOKEN' for OpenAI API.
    
    > 'TELEGRAM_API_TOKEN' for Telegram API.

    > 'PERSPECTIVE_API_TOKEN' for [Google Perspective API](https://www.perspectiveapi.com).

__Message Handler ('handle_text_messages'):__
1. Function Purpose:
    >Handles incoming text messages from users.

    >Validates message length and correctness.

2. Group Information Retrieval:
    >Retrieves previously saved group information from Redis.

    >Throws an exception if data is missing or invalid.

3. Swearing Detection ('swearing_local_test'):
    >Splits the message into words and checks against the loaded list of offensive words.

    >If offensive words are found, calls 'handle_method' for message processing.

4. Local Check Flow:
    >If no offensive words are found locally, invokes 'perspectiveapi' for additional toxicity evaluation.

__Loading Offensive Vocabulary:__
> Initially, the bot loads a list of offensive words from the Redis database.

__Handling Methods ('handle_method'):__

_Executes actions based on group-specific settings:_
>Deletes the message.

>Sends a warning.

>Calls 'OpenAI' api for replacement if specified.

__Perspective API Usage ('perspectiveapi'):__
>Sends the message text to Google Perspective API for toxicity analysis.

>Compares the toxicity level against the group's defined threshold.

>If the message is toxic, triggers 'handle_method'.

__OpenAI API Usage ('openaiapi'):__
>If specified by the method, utilizes OpenAI API to replace offensive language with neutral equivalents.

>Sends the processed message back to the group.


__Error Logging ('log_error'):__
>Logs errors occurring during any stage of message processing.

>Sends error messages to the bot administrator for further analysis and resolution.



__Clone the Repository:__

```bash
git clone https://github.com/aalex0372/Animated-Spoon.git
cd Animated-Spoon
```
```bash
pip install -r requirements.txt
```
```bash
pip install --upgrade -r requirements.txt
```


# Conclusion:
___This bot efficiently utilizes asynchronous operations to handle message processing, API calls, and real-time data management. It ensures a high degree of automation and message security within Telegram chats, effectively monitoring and filtering offensive content while preserving message integrity and structure.___
