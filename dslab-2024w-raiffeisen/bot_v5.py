import constants.constants as constants
import prompts.prompt_classifier as prompt_classifier
import prompts.prompt_banking as prompt_banking
import prompts.prompt_cards as prompt_card
import prompts.prompt_oeffnungszeiten as prompt_oeffnungszeiten

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType, Tool
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory

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

    return chat.predict_messages(messages)


"""
tools = [
    Tool(name="card_information",
         func=card_information,
         description="Beantwortet vollständig ausformulierte  Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten."
         ),

    Tool(name="banking_information",
         func=banking_information,
         description="Beantwortet vollständig ausformulierte Fragen zu dem Thema: Sperren des Online-Bankings."
         ),

    Tool(name="information_regarding_branches",
         func=information_regarding_branches,
         description="Beantwortet vollständig ausformulierte Fragen zu dem Thema: Bankfilialen (Öffnungszeiten, Ausstattung, etc.)."
         )
    ]
"""
tools = [card_information, banking_information, information_regarding_branches]


agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

memory.chat_memory.add_message(SystemMessage(content=prompt_classifier.system_message))
memory.chat_memory.add_message(first_ai_msg := AIMessage(content="Hier ist der Chatbot der Raiffeisenlandesbank Niederösterreich-Wien. Gerne beantworte ich Ihre Fragen zur Sperre von Karten sowie zur Ausstattung von Filialen."))

print(first_ai_msg.content)

agent = initialize_agent(
    tools,
    chat,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)
while True:
    msg = str(input("Your question: "))
    print(agent.run(msg))
    #print(memory)

    #print(memory.chat_memory)

    if len(memory.chat_memory.messages) > 4:
        del memory.chat_memory.messages[2]
        del memory.chat_memory.messages[2]