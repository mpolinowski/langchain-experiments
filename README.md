# LangChain — Hands-on Experiments

> 🎓 Hands-on experiments on the building blocks of LLM agents
> in Python, on [LangChain 1.x](https://python.langchain.com/docs/).
> Each folder is a self-contained [`uv`](https://docs.astral.sh/uv/) package that
> builds **one** idea on top of the last, from a single chat call up to a
> tool-calling agent. Gets to know what each library piece actually does.

* [Concepts overview](https://python.langchain.com/docs/concepts/)
* [Chat model integrations](https://python.langchain.com/docs/integrations/chat/)
* [LCEL / runnables](https://python.langchain.com/docs/concepts/lcel/)
* [Structured output](https://python.langchain.com/docs/concepts/structured_output/)
* [Agents](https://python.langchain.com/docs/concepts/agents/)

---

## 🛠️ What is LangChain used for?

**LangChain** is the glue between a raw LLM and a useful application. It wraps chat
models, prompts, and tools behind a small set of composable primitives, so the *same*
model can serve a one-shot call, a fixed pipeline, or a self-directed agent.

| Building block | What it is |
| :-- | :-- |
| **Chat model** 🗣️ | A typed wrapper around an LLM (here, a local Ollama) — `.invoke()` / `.stream()`. |
| **Structured output** 📐 | Force the model to answer as a Pydantic schema instead of free text. |
| **Chain (LCEL)** 🔗 | `Runnable` components (prompt → model → parser) piped into a sequence. |
| **Agent** 🤖 | Model + tools that *decides* which tool to call, in a reasoning loop. |
| **Tool** 🔧 | A callable the agent can invoke — a function, a SQL toolkit, a search. |

This repo is that stack in miniature: **talk to a model** → **chain it** → **give it tools**.

---

## 📚 Research — a tour of the folders

**The learning ladder (suggested order):**

```
🗣️ 01_getting_to_know_langchain   one chat call + structured output   (hello world)
🔗 02_basic_chains                LCEL chains + conditional branching
🕵️ 03_react                       agents + tools                      (web, SQL)
```

| 📁 Repo | What's inside | 🎯 Takeaway |
| :-- | :-- | :-- |
| **01_getting_to_know_langchain** 🗣️ | `init_chat_model(...)` pointed at a local Ollama (OpenAI-compatible). A Star-Trek system+human prompt (Worf tells a joke) answered through `with_structured_output(Pydantic)`, then the result's **type** and **fields** are printed. | The **hello world**: one chat model + **structured output** in a single `.invoke()`. |
| **02_basic_chains** 🔗 | An **LCEL** pipeline (`ChatPromptTemplate → structured-out LLM → parser → RunnableBranch`). It first classifies a tech review as *positive / negative*, then **branches**: positive → a **LinkedIn post** (senior experts), else a **Gen-Z Twitter post**. | **Chaining runnables** and **conditional branching** on a structured signal. |
| **03_react** 🕵️ | **Tools + agents.** Web tools (`DuckDuckGoSearchRun`, `WikipediaQueryRun`) and custom `@tool`s (a mock "email" + a capital-city population lookup) bound with `.bind_tools()`. Plus a `create_agent` **ReAct** loop over a seeded **SQLite** `events.db` via `SQLDatabaseToolkit`, screening for a license plate. | **ReAct agents**: bind tools, let the model *choose* them — including a real SQL toolkit. |

---

## 🧰 Run it

Every folder is its own `uv` **package** (**Python 3.14**, a `uv.lock` in each). They
all assume a **local Ollama** serving **`qwen3.8:latest`** on the OpenAI-compatible
endpoint `http://localhost:11434/v1` — that's hardcoded in each module, so to point
anywhere else just edit those kwargs.

```sh
# once, so Ollama is answering on :11434
ollama serve           # if it isn't already running
ollama pull qwen3.8:latest

# then, from inside a folder:
cd 01_getting_to_know_langchain
uv sync                # fills this folder's own .venv
uv run python -m 01_getting_to_know_langchain.main
```

> 💡 The `[project.scripts]` entry points (`01-…`, `02-…`, `03-react`) point at a
> leftover `main()` stub in `__init__.py` that only prints "Hello from…" — run the real
> experiments as modules (`python -m <pkg>.<module>`) as above.

**Folder 03 has two scenarios** plus a seeded DB. From inside `03_react/`:

```sh
# seed + inspect the SQLite events table  (CWD-relative path → run from the folder)
uv run python src/03_react/init_db.py
uv run python src/03_react/test_db.py

# the two agent examples
uv run python -m 03_react.main         # web / custom tools + .bind_tools()
uv run python -m 03_react.sql_agent    # create_agent + SQL toolkit over events.db
```

> ⚠️ `03_react`'s web tools (`ddgs`, `wikipedia`) need **real outbound internet**. The
> code falls back to the local mock tools when that isn't available — see the note in
> `main.py`.
