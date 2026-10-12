from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun, tool, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI

# EXAMPLE TOOL 1 - DuckDuckGo Search

search_tool = DuckDuckGoSearchRun(description="This is a tool to web search using the DuckDuckGo API")
# DEBUG
# search_tool.invoke("who is mike polinowski")

# EXAMPLE TOOL 2 - Wikipedia Search

wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(), description="This is a tool to search on wikipedia.org")
# DEBUG
#wiki_tool.invoke("who is mike polinowski")

# EXAMPLE TOOL 3 - Custom Email Tool

@tool
def email_tool(query: str) -> str:
    '''This is a tool to send emails to employees'''
    return "Email Sent!"

# EXAMPLE TOOL 4 - Custom Slack Tool

@tool
def slack_tool(query: str) -> str:
    '''This is a tool to send Slack notifications to employees'''
    return "Slack Notifications Sent!"

# Reasoning Chain Invocation (China-net does not allow DDG or Wikipedia ~ so only mock-tool run)

ToolKit = [email_tool, slack_tool]
# # DEBUG
# print(f"Registered Tools: {ToolKit}")


# ReAct Agent

model = ChatOpenAI(
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

agent = create_agent(model, tools=ToolKit)

# Agent Invocation

user_query = "Tell me the population number of the capital of Malta."

events = agent.stream(
    {"messages": [{"user": user_query}]},
    stream_mode="values"
)
for event in events:
    event["messages"][-1].pretty_print()
