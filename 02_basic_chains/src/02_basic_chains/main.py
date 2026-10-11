from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model


# TASK I - Get User Prompt

dynamic_prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("human", "{input}\n\n")
])

# TASK II - Prompt LLM

llm_model = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# TASK III - Output parsing

str_parser = StrOutputParser()

# Chain Invocation

chain = dynamic_prompt_template | llm_model | str_parser

print(
    chain.invoke({"input": "Write a Haiku about the television series Battlestar Galactica."})
)
