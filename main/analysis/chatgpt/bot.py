import openai
from .gpt_api_key import *
from ..utils.util import *


def ask_industry(name, desc):

    openai.api_key = key

    question = f"Use this text to answer my question: {desc}"

    messages = []
    cresponse = GetMessageMemory(question, messages)
    messages.append({"role": "assistant", "content": cresponse})

    cresponse = GetMessageMemory(
        f"What specific industries would you classify {name} in?", messages)
    messages.append({"role": "assistant", "content": cresponse})

    cresponse = GetMessageMemory(
        f"Can you give me the industris in a numbered list?", messages)
    messages.append({"role": "assistant", "content": cresponse})

    res_industries = get_list_from_numbered_list(cresponse)

    return res_industries


def GetMessageMemory(NewQuestion, lastmessage):
    lastmessage.append({"role": "user", "content": NewQuestion})

    msgcompetion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=lastmessage
    )

    msgresponse = msgcompetion.choices[0].message.content

    return msgresponse


def classify_headlines(headlines, company):
    openai.api_key = key
    headlines_classification = {}
    for headline in headlines[:10]:
        question = f"Here is a news headline for {company}: '{headline}', can you classify it as either positive, negative, or neutral based on public perception \n"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        classification = response.choices[0].message.content
        res = "positive" if "positive" in classification.lower() else "negative"
        headlines_classification[headline] = res
    return headlines_classification


def get_ticker_symbol(etf):
    openai.api_key = key
    question = f"What is the ticker symbol for {etf}? Only give me the answer"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    return answer.replace(" ", "")
