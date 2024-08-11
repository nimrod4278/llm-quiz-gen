from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage

chat = ChatLiteLLM(model="gpt-3.5-turbo")

messages = [
    HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )
]

print(chat.invoke(messages))