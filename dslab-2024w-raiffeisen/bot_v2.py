import constants.constants as constants
import prompts.prompt_classifier as prompt_classifier
import prompts.prompt_banking as prompt_banking
import prompts.prompt_cards as prompt_card
import prompts.prompt_oeffnungszeiten as prompt_oeffnungszeiten

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

chat = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY)


@tool
def card_information(question):
    """Beantwortet Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten."""
    messages = [
        SystemMessage(content=prompt_card.prompt_cards),
        HumanMessage(content=question)
    ]

    return chat.predict_messages(messages)


@tool
def banking_information(question):
    """Beantwortet Fragen zu dem Thema: Sperren des Online-Bankings."""
    messages = [
        SystemMessage(content=prompt_banking.prompt_banking),
        HumanMessage(content=question)
    ]

    return chat.predict_messages(messages)

@tool
def information_regarding_branches(question):
    """Beantwortet Fragen zu dem Thema: Bankfilialen (Öffnungszeiten, Ausstattung, etc.)"""
    messages = [
        SystemMessage(content=prompt_oeffnungszeiten.prompt_oeffnungszeiten),
        HumanMessage(content=question)
    ]

    #return chat.batch([messages,messages,messages,messages])
    #batch funktion zum testen
    return chat.predict_messages(messages)


tools = [card_information, banking_information, information_regarding_branches]

messages = [
    SystemMessage(content=prompt_classifier.system_message),
    first_ai_msg := AIMessage(content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Karten sowie zur Ausstattung von Filialen."),
]


print(first_ai_msg.content)
question_of_user = str(input(""))
messages.append(HumanMessage(content=question_of_user))


mrkl = initialize_agent(tools, chat, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
print(mrkl.run(messages))