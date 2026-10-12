from pathlib import Path
from langchain.agents import create_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI


# Connect to DB

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "events.db"
sql_db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

model = ChatOpenAI(
    model="qwen3.8:latest",
    temperature=0.6,
    top_p=0.95,
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

toolkit = SQLDatabaseToolkit(db=sql_db, llm=model)

# ## DEBUG
# print(toolkit.get_tools())


# ReAct Agent

system_message = "You are an security guard screening the alarm events database for detected liccense plates and face ids."
user_query = "Has the license plate SU:GB:678 been detected in an alarm event?"

agent = create_agent(model, toolkit.get_tools(), system_prompt=system_message)

results = agent.stream(
    {"messages": [("user", user_query)]},
    stream_mode="values"
)

for result in results:
    result["messages"][-1].pretty_print()
