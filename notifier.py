# Notify targets (maybe through telegram) and send audio file and transcript
import json
import asyncio
from aiogram.utils import exceptions, executor
from aiogram import Bot, Dispatcher, types

# TODO: send audio file


def notify(path, bot, dp, keywords=None, no_trigger=False):

    if keywords is None:
        if no_trigger:
            keywords = ["any"]
    a_file = open("keywords.json", "r")
    output = a_file.read()
    a_file.close()
    dic = dict(json.loads(output))
    targets = []
    for keyword in keywords:
        temp_targets = ((dic[keyword]).replace(" ","").split(","))
        for temp_target in temp_targets:
            if temp_target not in targets:
                targets.append(temp_target)

    with open((path + "transcript.txt"), "r") as f:
        transcript_list = f.readlines()
    f.close()
    transcript = ""
    for line in transcript_list:
        transcript += (line + "\n")

    if no_trigger:
        message = "New message: \"" + transcript + "\""
        for target in targets:
            executor.start(dp, send_message(bot, target, message, True))
            print("pretend I notify " + target + " with message \"" + message + "\".")
    else:

        for target in targets:
            keywords_present = []
            for keyword in keywords:
                if target in ((dic[keyword]).replace(" ", "").split(",")):
                    keywords_present.append(keyword)
            string_keywords_present = ", ".join(keywords_present)
            message = "Keywords \"" + string_keywords_present + "\" detected in: \"" + transcript + "\""
            executor.start(dp, send_message(bot, target, message))
            print("pretend I notify " + target + " with message \"" + message + "\".")


async def send_message(bot_in, user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param bot_in:
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """

    try:
        await bot_in.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        print(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        print(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        print(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(bot_in, user_id, text, disable_notification=disable_notification)  # Recursive call
    except exceptions.UserDeactivated:
        print(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        print(f"Target [ID:{user_id}]: failed")
    else:
        print(f"Target [ID:{user_id}]: success")
        return True
    return False

