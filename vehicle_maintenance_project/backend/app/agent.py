# Lightweight AI agent wrapper.
# Tries to use langchain if installed; otherwise provides a simple fallback agent.
import os

def simple_agent_run(message: str) -> str:
    # Very small heuristic agent: detect "calc:" or "calculate:" prefix or echo.
    text = message.strip()
    if text.lower().startswith(("calc:", "calculate:", "calculator:")):
        expr = text.split(":",1)[1].strip()
        try:
            # safe eval: allow only digits and operators
            allowed = set("0123456789+-*/(). ")
            if any(ch not in allowed for ch in expr):
                return "Calculator error: invalid characters."
            result = eval(expr)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculator error: {e}"
    # fallback echo
    return f"Agent (stub) echo: {message}"

# Try optional LangChain/OpenAI usage
try:
    from langchain import OpenAI
    from langchain.agents import Tool, initialize_agent
    def create_agent():
        llm = OpenAI(temperature=0)
        tools = [
            Tool(name="calculator", func=lambda q: simple_agent_run(f"calc: {q}"), description="Simple calc"),
        ]
        agent = initialize_agent(tools, llm, agent="conversational-react-description", verbose=False)
        return agent
    AGENT = create_agent()
    def agent_run(message: str) -> str:
        try:
            return AGENT.run(message)
        except Exception as e:
            return f"Agent error: {e}"
except Exception:
    AGENT = None
    def agent_run(message: str) -> str:
        return simple_agent_run(message)
