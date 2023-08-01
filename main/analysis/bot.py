import os
import openai
from .api_key import api_key

CLASSIFY_INDUSTRY = "Based on the following description of the company, what specific industry would you classify the company in?"


def ask_industry(name, desc):

    openai.api_key = api_key

    f = open(f"{name}-bot.txt", "w")
    f.write(name)
    f.write("\n")

    f.write(desc)
    f.write("\n")

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


def GetMessageMemory(NewQuestion, lastmessage):
    lastmessage.append({"role": "user", "content": NewQuestion})

    msgcompetion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lastmessage
    )

    msgresponse = msgcompetion.choices[0].message.content

    print("Question: " + NewQuestion)

    return msgresponse
