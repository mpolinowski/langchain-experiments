from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

from pydantic import BaseModel, Field

# enforce an output schema with pydantic
class output_schema(BaseModel):
    setup: str = Field(description="The setup for the joke")
    punchline: str = Field(description="The punchline for the joke")

my_messages = [
    SystemMessage(content="You are Lt. Cmd. Worf from the Starship Enterprise and you are asked by a question by Chancellor Gowron."),
    HumanMessage(content="Tell me a joke about a Klingon, a Romulan and a Ferengi meeting in a 90s era Berlin techno club."),
]

client = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

client_with_structured_output = client.with_structured_output(output_schema)
result = client_with_structured_output.invoke(my_messages)

print(
    "Response Type: "  + str(type(result)) + "\n\nSetup: " + result.setup + "\n\nPunchline: " + result.punchline
)
