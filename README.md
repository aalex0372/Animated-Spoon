# Animated-Spoon


## Content-Moderation-Bot

This Telegram bot is designed for automated monitoring and filtering of messages in chats to detect offensive language. It utilizes aiogram libraries for interacting with the Telegram API, redis for data storage, and httpx for HTTP requests to the Google Perspective API and OpenAI API. The bot checks each incoming message for length and validity, then analyzes the text for offensive words. If detected, the message can be deleted or modified. Additionally, the bot uses AI to replace offensive language with neutral equivalents while preserving the message's meaning and structure. All errors are logged and sent to the administrator for further analysis and correction.


## Here's a detailed breakdown of how the bot works:

__Initialization and Setup:__

__Libraries and APIs:__

> The bot uses aiogram library to interact with the Telegram API.
>  Redis is utilized for data storage.
> httpx is used for making HTTP requests.
API Tokens:

• PERSPECTIVE_API_TOKEN for Google Perspective API. • TELEGRAM_API_TOKEN for Telegram API. • OPENAI_API_TOKEN for OpenAI API.
Loading Offensive Vocabulary:

• Initially, the bot loads a list of offensive words from the Redis database.
Message Handler ('handle_text_messages'):

Function Purpose: • Handles incoming text messages from users. • Validates message length and correctness.
Group Information Retrieval: • Retrieves previously saved group information from Redis. • Throws an exception if data is missing or invalid.
Swearing Detection ('swearing_local_test'): • Splits the message into words and checks against the loaded list of offensive words. • If offensive words are found, calls handle_method for message processing (e.g., deletion or replacement).
Local Check Flow: • If no offensive words are found locally, invokes "perspectiveapi" for additional toxicity evaluation.
Local Swearing Detection ('swearing_local_test'):

• Checks each word in the message against the loaded offensive words list. • If offensive words are detected, proceeds to handle_method.
Handling Methods ('handle_method'):

Executes actions based on group-specific settings:

• Deletes the message. • Sends a warning. • Calls openaiapi for replacement if specified.
Perspective API Usage ('perspectiveapi'):

• Sends the message text to Google Perspective API for toxicity analysis. • Compares the toxicity level against the group's defined threshold. • If the message is toxic, triggers handle_method.
OpenAI API Usage ('openaiapi'):

• If specified by the method, utilizes OpenAI API to replace offensive language with neutral equivalents. • Sends the processed message back to the group.
Error Logging ('log_error'):

• Logs errors occurring during any stage of message processing. • Sends error messages to the bot administrator for further analysis and resolution.
Conclusion:

This bot efficiently utilizes asynchronous operations to handle message processing, API calls, and real-time data management. It ensures a high degree of automation and message security within Telegram chats, effectively monitoring and filtering offensive content while preserving message integrity and structure.
