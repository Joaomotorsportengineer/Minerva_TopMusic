import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") 


model = ChatOpenAI(
    model="gpt-4.1",
    api_key=OPENAI_API_KEY
    )
# Use o caminho do seu banco
db = SQLDatabase.from_uri("sqlite:///BaseDados/top_musicas.db")


toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=10,
)

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
)



st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Pergunte sobre as músicas do banco (ex.: quantas músicas temos?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta_final = ""
            for step in agent.stream(
                {"messages": [{"role": "user", "content": prompt}]},
                stream_mode="values",
            ):
                messages = step.get("messages", [])
                if messages:
                    ultima = messages[-1]
                    if hasattr(ultima, "content") and ultima.content:
                        resposta_final = ultima.content
            if not resposta_final and messages:
                resposta_final = str(messages[-1])
            st.write(resposta_final or "Sem resposta.")

    st.session_state.messages.append({"role": "assistant", "content": resposta_final or "Sem resposta."})