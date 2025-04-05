from duckduckgo_search import DDGS
from smolagents import load_tool, CodeAgent, HfApiModel, DuckDuckGoSearchTool
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path

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

agent = CodeAgent(
    tools=[search_tool],
    model=HfApiModel(model_id="Qwen/Qwen2.5-72B-Instruct"),
    planning_interval=3,  # This is where you activate planning!
)

# Run it!
result = agent.run(
    "How long would a cheetah at full speed take to run the length of Pont Alexandre III?",
)
logger.info(result)
logger.info(agent.memory.steps)
