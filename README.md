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





