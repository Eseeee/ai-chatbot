# Importing packages by third parties
import openai
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

# Importing packages created by us
import constants.constants as constants
import prompts.prompt_banking as prompt_banking
import prompts.prompt_cards as prompt_cards
import functions.functions as functions

question_of_user = str(input("Question: "))

# Instantiating the model

completion = openai.ChatCompletion.create(
    model=constants.MODEL,
    api_key=constants.OPENAI_API_KEY,
    # For better structure, the list of functions has been defined in functions/functions.py
    functions=functions.function_definition,
    messages=[
        {
            "role": "system",
            "content": """
            Du bist ein Chatbot, der auf der Website der 'Raiffeisen Bank Wien Niederösterreich' implementiert ist. Du beachstest folgende Regeln:

            (1) Du beantwortest NUR Fragen zur Sperrung von Debit- oder Kreditkarten oder zur Sperrung des Online-Bankings.
            (2) Du beantwortest NUR Fragen, wenn du dir absolut sicher bist.
            (3) Um die Fragen zu beantworten, rufst du die entsprechenden Funktionen auf. Die Fragen, die du an die Funktionen weitergibst, müssen vollständig ausformuliert sein.
            """
        },
        {
            "role": "user",
            "content": question_of_user

        }

    ],
    # randomness as low as possible
    temperature=0
)

def debit_card_information(question):
    llm = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY, model = constants.MODEL)
    """Beantwortet Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten."""
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(prompt_cards.prompt_cards)
            ),
            HumanMessagePromptTemplate.from_template("Die Frage lautet:\n{text}"),
        ]
    )
    return llm(chat_template.format_messages(text=question))

def banking_information(question):
    llm = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY,model = constants.MODEL)
    """Beantwortet Fragen zu dem Thema: Sperren des Online-Bankings."""
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(prompt_banking.prompt_banking)
            ),
            HumanMessagePromptTemplate.from_template("Die Frage des Nutzers lautet:\n{text}"),
        ]
    )
    return llm(chat_template.format_messages(text=question))


completion = completion["choices"][0]["message"]


if completion.get("function_call"):
    function_name = eval(completion["function_call"]["name"])
    question = json.loads(completion["function_call"]["arguments"]).get("question")

    function_response = function_name(question)

    print(function_response.content)
else:
    print(completion["content"])