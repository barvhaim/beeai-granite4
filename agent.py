import asyncio
import logging
import os
import sys
import traceback
from typing import Any

from dotenv import load_dotenv

from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.emitter import EmitterOptions, EventMeta
from beeai_framework.errors import FrameworkError
from beeai_framework.logger import Logger
from beeai_framework.memory import TokenMemory
from beeai_framework.tools import AnyTool
from beeai_framework.tools.weather import OpenMeteoTool
from helpers.io import ConsoleReader

# Load environment variables
load_dotenv()

# Configure logging - using DEBUG instead of trace
logger = Logger("app", level=logging.DEBUG)

reader = ConsoleReader()


def create_agent() -> ReActAgent:
    """Create and configure the agent with tools and LLM"""
    llm = ChatModel.from_name(
        "ollama:granite4:micro",
        ChatModelParameters(temperature=0),
    )

    # Configure tools
    tools: list[AnyTool] = [
        OpenMeteoTool(),
    ]

    # Create agent with memory and tools
    agent = ReActAgent(llm=llm, tools=tools, memory=TokenMemory(llm))

    return agent


def process_agent_events(data: Any, event: EventMeta) -> None:
    """Process agent events and log appropriately"""

    if event.name == "error":
        reader.write("Agent: ", FrameworkError.ensure(data.error).explain())
    elif event.name == "retry":
        reader.write("Agent: ", "retrying the action...")
    elif event.name == "update":
        reader.write(f"Agent({data.update.key}): ", data.update.parsed_value)
    elif event.name == "start":
        reader.write("Agent: ", "starting new iteration")
    elif event.name == "success":
        reader.write("Agent: ", "success")


async def main() -> None:
    """Main application loop"""

    # Create agent
    agent = create_agent()

    # Log code interpreter status if configured
    code_interpreter_url = os.getenv("CODE_INTERPRETER_URL")
    if code_interpreter_url:
        reader.write(
            "System: ",
            f"The code interpreter tool is enabled. Please ensure that it is running on {code_interpreter_url}",
        )

    reader.write(
        "System: ", "Agent initialized with Wikipedia, DuckDuckGo, and Weather tools."
    )

    # Main interaction loop with user input
    for prompt in reader:
        # Run agent with the prompt
        response = await agent.run(
            prompt,
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20,
        ).on("*", process_agent_events, EmitterOptions(match_nested=False))

        reader.write("Agent: ", response.last_message.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
