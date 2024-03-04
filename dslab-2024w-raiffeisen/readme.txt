bot_v1 -> Kann nur eine Frage (dh kein chatbot) zu einem Thema beantworten
    implementiert mit OpenAI package (FunctionCalling) und Langchain (Prompts)

bot_v2 -> Kann nur eine Frage (dh kein Chatbot), aber zu mehreren Themen beantworten
    Implementiert nur mit langchain (AgentType.OPENAI_FUNCTIONS)

bot_v3 -> Kann mehrere Fragen (dh EIN Chatbot) zu mehreren Themen beantworten.
    Implementiert mit AgentType.OPENAI_FUNCTIONS

    Allerdings ist die memory-Struktur nicht gut, da für jede Anfrage der gesamte bisherige Chatverlauf geschickt wird (hoher Tokenverbrauch). Implementierung mit 
    OpenAIFunctions auf Langchain (geht ganz gut).
    
    Problem, dass Funktionen immer gecalled werden.

bot_v4 -> Kann mehrere Fragen (dh EIN Chatbot) zu mehreren Themen beantworten
    Implementierung mit AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
        Funktioniert manchmal, allerdings manchmal auch parsing error
    Memory auf die letzten zwei Chats beschränkt, aber flexibel einstellbar
    Zudem halluziniert das model oft

bot_v5 -> Weiterentwicklung von v3, implementiert mit AgentType.OPENAI_FUNCTIONS
    funktioniert bis jetzt am besten
    Memory auf die letzten zwei Chats beschränkt, aber flexibel einstellbar
    
    MMn die beste Grundlage für weitere Module
    
Bot_2_Test_OG --> bot_v2 mit Prompt Engineering, trainert auf Öffnungszeiten Schemata der anderen funktionen übernommen

Bot_2_Test_v1 --> bot_v2 mit Öffnungszeiten, basieren auf llama und vectorestore

Bot_2_Test_v2 --> bot_v2 mit Öffnungszeiten, basierend auf sqlite im backend
