import constants.constants as constants
import prompts.prompt_classifier as prompt_classifier
import prompts.prompt_banking as prompt_banking
import prompts.prompt_cards as prompt_card

from langchain.tools import tool
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory

chat1 = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY) # for functions
chat2 = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY) # for chat model
chat3 = ChatOpenAI(openai_api_key=constants.OPENAI_API_KEY) # for memory

msg = [
    SystemMessage(content=prompt_classifier.system_message),
    first_ai_msg := AIMessage(content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Debit- und Kreditkarten sowie zur Sperre des Online-Bankings."),
]

@tool
def card_information(question):
    """Beantwortet nur Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten."""
    messages = [
        SystemMessage(content=prompt_card.prompt_cards),
        HumanMessage(content=question)
    ]

    return chat1.predict_messages(messages)


@tool
def banking_information(question):
    """Beantwortet nur Fragen zu dem Thema: Sperren des Online-Bankings."""
    messages = [
        SystemMessage(content=prompt_banking.prompt_banking),
        first_ai_msg := AIMessage(
            content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Debit- und Kreditkarten sowie zur Sperre des Online-Bankings."),
    ]

    return chat1.predict_messages(messages)


tools = [
    Tool(name="card_information",
         func=card_information,
         description="Beantwortet Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten."
         ),

    Tool(name="banking_information",
         func=banking_information,
         description="Beantwortet Fragen zu dem Thema: Sperren des Online-Bankings."
         )
    ]

#tools = [card_information, banking_information]

#memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=2)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.chat_memory.add_message(SystemMessage(content=prompt_classifier.system_message))
memory.chat_memory.add_message(first_ai_msg := AIMessage(content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Debit- und Kreditkarten sowie zur Sperre des Online-Bankings."),)


print(first_ai_msg.content)

react = initialize_agent(
    tools,
    chat2,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)

while True:
    print(react.run({"input": str(input("Your question: ")), "chat_history":msg}), end = "\n")
    #print(msg)

    if len(memory.chat_memory.messages) > 4:
        del memory.chat_memory.messages[2]
        del memory.chat_memory.messages[2]