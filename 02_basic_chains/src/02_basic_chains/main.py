from typing import Dict

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain.chat_models import init_chat_model


# TASK I - Get User Prompt

dynamic_prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("human", "{input}")
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

output_parser = StrOutputParser()

# Task IV - Dictinary maker

def dictionary_maker(text: str) -> Dict:
    return {"text": text}

runable_dictionary_maker = RunnableLambda(dictionary_maker)


# Task V - Apply post template

prompt = ChatPromptTemplate.from_messages(
    messages = [
        ("system", "You are a social media post generator."),
        ("human", "Create a Twitter post for the following: {text}")
    ]
)

# Task VI - Generate the post

llm_model = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Task VII - Output parsing

output_parser = StrOutputParser()

# Sequence Invocation

sequence = RunnableSequence(
    dynamic_prompt_template,
    llm_model,
    output_parser,
    runable_dictionary_maker,
    prompt,
    llm_model,
    output_parser

)

print(
   sequence.invoke({"input": "Write 1 paragraph long summary to introduce the library LangGraph and what it brings to the table on top of LangChain."})
)
