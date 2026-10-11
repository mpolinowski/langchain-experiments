from openai import OpenAI

# Ollama speaks the OpenAI HTTP API at http://localhost:11434/v1.
# No real API key is needed for a local server, but the openai client
# refuses to start with a missing/empty key, so pass a placeholder
# string -- Ollama ignores it.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # placeholder; Ollama does not validate it
)

chat_completion = client.chat.completions.create(
    model="qwen3.8:latest",
    messages=[
        {
            "role": "user",
            "content": "Hello there! Please tell me a joke an AI agent walking into the DMV office wanting to renew their drivers license.",
        }
    ],
)

print(chat_completion.choices[0].message.content)
