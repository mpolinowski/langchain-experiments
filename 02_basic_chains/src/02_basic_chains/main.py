from typing import Dict

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
from langchain.chat_models import init_chat_model

#########################################################################
#########################################################################

# Chain with Parallel Outputs

## TASK I - Get User Prompt

dynamic_prompt_template = ChatPromptTemplate([
    ("system", "You are a technology journalist that creates social media posts."),
    ("human", "Please summarize the following technology: {input}")
])

## TASK II - Prompt LLM

llm_model = init_chat_model(
    model_provider="openai",
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

## TASK III - Output parsing

output_parser = StrOutputParser()

# Task IV - Dictinary maker

def dictionary_maker(text: str) -> Dict:
    return {"text": text}

runable_dictionary_maker = RunnableLambda(dictionary_maker)

#########################################################################
#########################################################################

# Parallel Output Chain I

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

    text = text["text"]

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

# Complete Chain Orchestration

complete_sequence = RunnableSequence(
    dynamic_prompt_template,
    llm_model,
    output_parser,
    runable_dictionary_maker,
    RunnableParallel(
        branches = {
            "linkedin": linkedin_sequence,
            "twitter": twitter_chain_runable
        })

)

# Additional Post-Processing running the complete chain as runable

def beautify_output(chain_output: dict) -> dict:
    linkedin_response = chain_output["branches"]["linkedin"]
    twitter_response = chain_output["branches"]["twitter"]

    return {"linkedin": linkedin_response, "twitter": twitter_response}

beautify_output_runnable = RunnableLambda(beautify_output)

post_sequence = RunnableSequence(
    complete_sequence,
    beautify_output_runnable

)

print(
   post_sequence.invoke({"input": "Write 1 paragraph long summary to introduce the library LangGraph and what it brings to the table on top of LangChain."})
)
