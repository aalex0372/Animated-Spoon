from aiogram.utils.exceptions import TelegramAPIError
from aiogram import Bot, Dispatcher, executor
from redis.asyncio import Redis
import datetime
import asyncio
import creds
import httpx
import json
import re 

TELEGRAM_API_TOKEN = creds.TELEGRAM_API_TOKEN
OPENAI_API_TOKEN = creds.OPENAI_API_TOKEN
PERSPECTIVE_API_TOKEN = creds.PERSPECTIVE_API_TOKEN

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

swearing_words = set()  # Load swearing words from Redis


async def load_swearing_words():
    global swearing_words
    redis = Redis(host='localhost', port=6379, db=0)
    swearing_words = {i.decode('utf-8') for i in await redis.smembers("swearing")}
    await redis.close()


@dp.message_handler(content_types=['text'])
async def handle_text_messages(message):
    if message.chat.type not in ['group', 'supergroup']:  # Check if the message is from a group or supergroup
        return  # Early exit if the message is not from a group or supergroup
    if not (message and message.text and message.chat.id and message.from_user.id):
        return  # Early exit if message isn't valid
    if not await valid_message_length(message):  # if message.text isn't in the range (2~>300) characters
        return  # Early exit if message length isn't valid
    try:
        redis = Redis(host='localhost', port=6379, db=0)
        json_data_redis = await redis.hget("groups_id", message.chat.id)  # Retrieves data from Redis
        await redis.close()  # (hash name + specific key)

        if not json_data_redis:  # Checking if json_data_redis is None or empty
            raise ValueError(f"No data found for chat ID: {message.chat.id}")  # Raises an error ValueError

        _, data_dict = json.loads(json_data_redis.decode('utf-8'))

        core_data = {"message_text": message.text, "message_id": message.message_id,
                     "group_id": message.chat.id, "user_id": message.from_user.id,
                     "user_first_name": message.from_user.first_name, "user_username": message.from_user.username,
                     "method": data_dict.get('method'), "toxic_lvl": data_dict.get('toxic_lvl'),
                     "reply_to_message_id": message.reply_to_message.message_id if message.reply_to_message else None}
        await swearing_local_test(core_data)  # Processing the data for a local test

    except json.JSONDecodeError as e:
        await log_error(e, "JSON parsing-groups_id-htm", message.chat.id)
    except ValueError as e:
        await log_error(e, "Redis data retrieval-htm", message.chat.id)
    except Exception as e:
        await log_error(e, "handle_text_messages-htm", message.chat.id)


async def valid_message_length(message):
    try:
        return 2 < len(re.sub(r'\W+', ' ', message.text)) < 300  # We get True if the range is (2~300) characters
    except Exception as e:
        await log_error(e, "valid_message_length-vml", message.chat.id)


async def swearing_local_test(core_data):
    try:
        cleaned_message_set = set(re.sub(r'\W+', ' ', core_data["message_text"].lower()).split())  # set of message
        if swearing_words & cleaned_message_set:  # Check for intersection
            await handle_method(core_data)  # Here we call a method func
        else:
            await perspectiveapi(core_data)  # Additional check for swearing
    except Exception as e:
        await log_error(e, "swearing_local_test-slt", core_data["group_id"])
    except json.JSONDecodeError as e:
        await log_error(e, "JSON parsing-groups_id-slt", core_data["group_id"])


async def handle_method(core_data):
    try:
        await bot.delete_message(core_data["group_id"], core_data["message_id"])  # Pre-deleting a message in all cases
        if core_data["method"] == 2:
            await bot.send_message(core_data["group_id"], "Oops! Looks like your message had some words "
                                                          "we usually avoid.")
        elif core_data["method"] == 3:
            await openaiapi(core_data)
    except Exception as e:
        await log_error(e, "handle_method-hd", core_data["group_id"])


async def perspectiveapi(core_data):
    analyze_request = {'comment': {'text': core_data["message_text"]}, 'requestedAttributes': {'TOXICITY': {}}}
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_TOKEN}"
            response = await client.post(url, json=analyze_request)
            response.raise_for_status()  # Raise an exception for any HTTP error
            response_data = response.json()
            toxicity_score = response_data['attributeScores']['TOXICITY']['summaryScore']['value']
            if toxicity_score > core_data["toxic_lvl"]:
                await handle_method(core_data)
            else:
                return
            await asyncio.sleep(0.9)  # Introduce a 1-second delay to comply with the API rate limit
    except httpx.HTTPStatusError as http_err:
        await log_error(http_err, "perspectiveapi", core_data["group_id"])
    except Exception as e:
        await log_error(e, "perspectiveapi", core_data["group_id"])


async def openaiapi(core_data):
    prompt = ("Replace any profanity or offensive language in the text with neutral analogs, preserving "
              "the original meaning and structure. Provide the edited text directly without any"  # Our prompt to OpenAI
              f" labels or introductory words and same language as a given text.\n\nText: {core_data['message_text']}")
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_TOKEN}", "Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={"model": "gpt-3.5-turbo",  # Model version
                      "messages": [{"role": "user", "content": prompt}],  # Our input message with user role and content
                      "max_tokens": 312,  # Sets the maximum len
                      "temperature": 0.45,  # Controls randomness
                      "top_p": 1,  # Sampling parameter, 1 = NO Sampling
                      "frequency_penalty": 0.1,  # Decreases the likelihood of repeating words
                      "presence_penalty": 0.1})  # Decreases the likelihood of repeating topics
            response.raise_for_status()  # Raise an exception for any HTTP error
            completion = response.json()
            msg = f'<a href="https://t.me/{core_data["user_username"]}">{core_data["user_first_name"]}</a> says: '
            await bot.send_message(core_data["group_id"], f"{msg}\n{completion['choices'][0]['message']['content']}",
                                   parse_mode='HTML', disable_web_page_preview=True,
                                   reply_to_message_id=core_data["reply_to_message_id"])  # Sends msg & AI's response

    except httpx.HTTPStatusError as http_err:
        error_message = f"HTTPStatusError: {http_err}\nResponse content: {http_err.response.content.decode()}"
        await log_error(error_message, "openaiapi_worker", core_data["group_id"])
    except Exception as e:
        await log_error(e, "openaiapi_worker", core_data["group_id"])


async def log_error(e, stage, chat_id):  # Attempts to log an error by sending a message to a specific ID
    """ :param e: An error
        :param stage: The code processing stage
        :param chat_id: The chat IDs we need to handle our error messages """
    group_id = chat_id if chat_id else "unknown"
    your_chat_group_id = int()  # chat/group you need for error handling  🤷🏽‍
    try:
        error_message = (f"Stage: {stage}. Group {group_id}\n\n"
                         f"Date: {datetime.datetime.now()}\n"
                         f"An error occurred - {type(e).__name__}"
                         f"\n\n{e}")
        await bot.send_message(your_chat_group_id, error_message)
    except TelegramAPIError as tg_error:  # Specific exception for Telegram API errors
        await bot.send_message(your_chat_group_id, f"TelegramAPIError:\n{str(tg_error)}")
    except Exception:  # If an error occurs while logging, it will be caught here and ignored.
        pass  # There is nothing we can do


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_swearing_words())  # Load swearing words once before starting the bot
    executor.start_polling(dp, skip_updates=True, loop=loop)
