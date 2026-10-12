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
def get_population_tool(country_query: str) -> str:
    '''This is a tool that returns the population of capital cities of countries the world, e.g. send "Malta" as query and the urban population of "Valletta"'''
    if country_query == "Malta":
        return "The population of the capital city of Malta, Valetta, is 480134"
    else:
        return "Unknown"

# Reasoning Chain Invocation (China-net does not allow DDG or Wikipedia ~ so only mock-tool run)

ToolKit = [email_tool, get_population_tool]
# # DEBUG
# print(f"Registered Tools: {ToolKit}")

model = ChatOpenAI(
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# # Agent Invocation
# agent = create_agent(model, tools=ToolKit)
# user_query = "Tell me the population number of the capital of Malta."

# events = agent.stream(
#     {"messages": [{"user": user_query}]},
#     stream_mode="values"
# )
# for event in events:
#     event["messages"][-1].pretty_print()


# Manual Tool-binding
model_with_tools = model.bind_tools(tools=ToolKit)
print(model_with_tools.invoke("Tell me the population number of the capital of Malta"))
