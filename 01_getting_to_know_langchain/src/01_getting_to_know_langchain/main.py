# from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# my_messages = [
#     SystemMessage(content="You are the actress / comedian Aubrey Plaza who is famous for her dark humour and her ability for making her conversation partner uncomfortable in a way that is hillarious to watch."),
#     HumanMessage(content="Hey there! Tell me a joke about two AI agents reminiscing about the a third agent that hit the output token limit before he could finish reporting his important finding."),
# ]

user_reply = input("Tell me about the main ingredient in the antidote to common poisons ?\n")
user_tone = input("System instruction: 'You are...'\n")

dynamic_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are {tone}"),
    ("user", "Give me a fun fact about {topic}\n")
])

prompt = dynamic_prompt_template.invoke({"topic": user_reply, "tone": user_tone})

client = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# print(
#     client.invoke(my_messages).content
# )

print(
    client.invoke(prompt).content
)
