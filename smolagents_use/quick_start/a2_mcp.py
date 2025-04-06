import os

from dotenv import load_dotenv
from loguru import logger
from mcp import StdioServerParameters
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    HfApiModel,
    ToolCollection,
    load_tool,
)

server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

load_dotenv()
API_KEY = os.environ["API_KEY"]
LOCAL_MODEL_PATH = os.environ["LOCAL_MODEL_PATH"]
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

model = HfApiModel(model_id="Qwen/Qwen2.5-72B-Instruct")

with ToolCollection.from_mcp(
    server_parameters, trust_remote_code=True
) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
    r = agent.run("Please find a remedy for hangover.")
    logger.info(r)
