from langchain_openai import ChatOpenAI

from env import OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)