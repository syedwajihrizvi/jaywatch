import openai
from api_key import *
from util import *


def ask_industry(name, desc):

    openai.api_key = key

    question = f"Use this text to answer my question: {desc}"

    messages = []
    cresponse = GetMessageMemory(question, messages)
    messages.append({"role": "assistant", "content": cresponse})

    cresponse = GetMessageMemory(
        f"What specific industries would you classify {name} in?", messages)
    messages.append({"role": "assistant", "content": cresponse})
    print(f"Response: {cresponse}")

    cresponse = GetMessageMemory(
        f"Can you give me the industris in a numbered list?", messages)
    messages.append({"role": "assistant", "content": cresponse})

    print(f"Response: {cresponse}")

    res_industries = get_list_from_numbered_list(cresponse)

    return res_industries


def GetMessageMemory(NewQuestion, lastmessage):
    lastmessage.append({"role": "user", "content": NewQuestion})

    msgcompetion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lastmessage
    )

    msgresponse = msgcompetion.choices[0].message.content

    print("Question: " + NewQuestion)

    return msgresponse
