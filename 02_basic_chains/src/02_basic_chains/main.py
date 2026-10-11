from typing import Dict, Literal
from pydantic import BaseModel

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableSequence, RunnableLambda, RunnableParallel
from langchain.chat_models import init_chat_model



#########################################################################
#########################################################################

# Chain with Conditional Output Chains

## TASK I - Get User Prompt

dynamic_prompt_template = ChatPromptTemplate([
    ("system", "You are a technology review evaluator."),
    ("human", "Please categorize the following technology review as positive or negative: {input}")
])

## TASK II - Prompt LLM

class output_schema(BaseModel):
    review_sentiment: Literal["positive", "negative"]

llm_model = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

llm_model_with_structured_output = llm_model.with_structured_output(output_schema)

# # DEBUG
# result = llm_model_with_structured_output.invoke("This technology stack is stupid! I hate it so much....")
# print(result)
# print(type(result))
# print(result.model_dump())
# print(result.model_dump()["review_sentiment"])

# Task IV - Return the "positiv" / "negative" string only

def pydantic_json(input: output_schema) -> str:
    print(input)
    print(type(input))
    return input.model_dump()["review_sentiment"]

# # DEBUG
# result = llm_model_with_structured_output.invoke("This technology stack is stupid! I hate it so much....")
# print(result)
# print(type(result))
# parsed = pydantic_json(result)
# print(parsed)

runable_pydantic_json = RunnableLambda(pydantic_json)

#########################################################################
#########################################################################

# Parallel Conditional Output Chain "positive"

# Task Ia - Apply post template

linkedin_prompt = ChatPromptTemplate.from_messages(
    messages = [
        ("system", "You are a technology journalist that creates LinkedIn posts targeting senior technology experts."),
        ("human", "Create a LinkeIn post for the following technology: {text}")
    ]
)

# Task IIa - Generate the post

llm_model = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Task IIIa - Output parsing

output_parser = StrOutputParser()

# Sequence Invocation

linkedin_sequence = RunnableSequence(
    linkedin_prompt,
    llm_model,
    output_parser
)

#########################################################################
#########################################################################

# Parallel Output Chain II

def twitter_chain(text: dict):

    # Task Ia - Apply post template

    twitter_prompt = ChatPromptTemplate.from_messages(
        messages = [
            ("system", "You are a Gen-Z technology journalist that creates Twitter posts targeting young and hip technology enthusiasts."),
            ("human", "Create a Twitter post for the following technology: {text}")
        ]
    )

    # Task IIa - Generate the post

    llm_model = init_chat_model(
        model_provider="openai",
        model="qwen3.8:latest",
        temperature=0.6,
        top_p=0.95,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    # Task IIIa - Output parsing

    output_parser = StrOutputParser()

    # Sequence Invocation

    twitter_sequence = RunnableSequence(
        twitter_prompt,
        llm_model,
        output_parser
    )

    return twitter_sequence.invoke(text)

twitter_chain_runable = RunnableLambda(twitter_chain)

#########################################################################
#########################################################################

# Conditional Chain Orchestration

conditional_chain = RunnableBranch(
    (lambda x: "positive" in x, linkedin_sequence),
    twitter_chain_runable
)

complete_sequence = RunnableSequence(
    dynamic_prompt_template,
    llm_model_with_structured_output,
    runable_pydantic_json,
    conditional_chain

)


print(
   complete_sequence.invoke({"input": "This technology stack is great! I love it so much...."})
)
