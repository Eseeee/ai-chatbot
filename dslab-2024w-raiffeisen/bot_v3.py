import constants.constants as constants
import prompts.prompt_classifier as prompt_classifier
import prompts.prompt_banking as prompt_banking
import prompts.prompt_cards as prompt_card
import functions.functions as functions

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

chat = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY)


@tool
def debit_card_information(question):
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


tools = [debit_card_information, banking_information]

messages = [
    SystemMessage(content=prompt_classifier.system_message),
    first_ai_msg := AIMessage(content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Debit- und Kreditkarten sowie zur Sperre des Online-Bankings."),
]

mrkl = initialize_agent(tools, chat, agent=AgentType.OPENAI_FUNCTIONS, verbose = True)

print(first_ai_msg.content)

while True:
    human_msg = str(input("Ihre Frage: "))
    print(human_msg)
    human_msg = HumanMessage(content=human_msg)
    messages.append(human_msg)
    print(ai_msg := mrkl.run(messages))
    messages.append(AIMessage(content = ai_msg))
    print(messages)