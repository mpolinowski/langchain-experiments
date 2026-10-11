from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI


# client = ChatOpenAI(
#     model="qwen3.8:latest",
#     temperature=0.6,
#     top_p=0.95,
#     base_url="http://localhost:11434/v1",
#     api_key="ollama"
# )

# print(client.invoke("Hello there! Please tell me a joke a Tesla automatic driver AI agent walking into the gas station byuing a streetmap."))

client = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

print(
    client.invoke("Hey there! Please tell me a joke about an AGI model sitting on the pavement at Times Square, an empty StarBucks cup in it's hand, begging for money because it lost it's job to a more efficient Support Vector Machine.").content
)
