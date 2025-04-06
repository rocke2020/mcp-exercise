from duckduckgo_search import DDGS
from smolagents import (
    load_tool,
    CodeAgent,
    HfApiModel,
    DuckDuckGoSearchTool,
    OpenAIServerModel,
)
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
import os

logger.add(
    Path(__file__).with_suffix(".log"), mode="w", encoding="utf-8", level="DEBUG"
)
load_dotenv()


def test_duckduck():
    ddgs = DDGS()
    query = "网上搜一下，周庄古镇和东方绿舟的距离"
    results = ddgs.text(query, max_results=10)
    print(results)


search_tool = DuckDuckGoSearchTool()

load_dotenv()
API_KEY = os.environ["API_KEY"]
LOCAL_MODEL_PATH = os.environ["LOCAL_MODEL_PATH"]
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
logger.info(f"{LOCAL_MODEL_PATH = }")

model = OpenAIServerModel(
    model_id=LOCAL_MODEL_PATH,
    api_base=BASE_URL,  # Leave this blank to query OpenAI servers.
    api_key=API_KEY,  # Switch to the API key for the server you're targeting.
)

agent = CodeAgent(
    tools=[search_tool],
    model=model,
    # planning_interval=3,  # This is where you activate planning!
)

# Run it!
result = agent.run(
    "How long would a cheetah at full speed take to run the length of Pont Alexandre III?",
)
logger.info(result)
logger.info(agent.memory.steps)
