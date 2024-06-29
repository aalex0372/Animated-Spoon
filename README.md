# Animated-Spoon

## Content-Moderation-Bot

___This Telegram bot is designed for automated monitoring and filtering of messages in chats to detect offensive language. It utilizes aiogram libraries for interacting with the Telegram API, redis for data storage, and httpx for HTTP requests to the Google Perspective API and OpenAI API. The bot checks each incoming message for length and validity, then analyzes the text for offensive words. If detected, the message can be deleted or modified. Additionally, the bot uses AI to replace offensive language with neutral equivalents while preserving the message's meaning and structure. All errors are logged and sent to the administrator for further analysis and correction.___


## Here's a detailed breakdown of how the bot works:

__Initialization and Setup:__
1. Libraries and APIs:
    >The bot uses 'aiogram' library to interact with the Telegram API.
    
    > 'redis' is utilized for data storage.

    > 'httpx' is used for making HTTP requests.

2. API Tokens:
    > 'TELEGRAM_API_TOKEN' for Telegram API.

    > 'PERSPECTIVE_API_TOKEN' for Google Perspective API.

    > 'PERSPECTIVE_API_TOKEN' for Google Perspective API.

__Loading Offensive Vocabulary:__
> Initially, the bot loads a list of offensive words from the Redis database.

__Message Handler ('handle_text_messages'):__
1. Function Purpose:
    >Handles incoming text messages from users.

    >Validates message length and correctness.

2. Group Information Retrieval:
    >Retrieves previously saved group information from Redis.

    >Throws an exception if data is missing or invalid.

3. Swearing Detection ('swearing_local_test'):
    >Splits the message into words and checks against the loaded list of offensive words.

    >If offensive words are found, calls 'handle_method' for message processing (e.g., deletion or replacement).

4. Local Check Flow:
    >If no offensive words are found locally, invokes 'perspectiveapi' for additional toxicity evaluation.

__Local Swearing Detection ('swearing_local_test'):__
>Checks each word in the message against the loaded offensive words list.

>If offensive words are detected, proceeds to 'handle_method'.

__Handling Methods ('handle_method'):__

>Executes actions based on group-specific settings:

>Deletes the message.

>Sends a warning.

>Calls 'OpenAI' api for replacement if specified.

