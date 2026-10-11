from langchain_openai import ChatOpenAI

client = ChatOpenAI(
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

print(client.invoke("Hello there! Please tell me a joke a Tesla automatic driver AI agent walking into the gas station byuing a streetmap."))
