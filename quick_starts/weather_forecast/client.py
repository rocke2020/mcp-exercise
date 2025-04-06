import os
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, OpenAIServerModel
from mcp import StdioServerParameters

# Load environment variables
load_dotenv()
API_KEY = os.environ["API_KEY"]
LOCAL_MODEL_PATH = os.environ["LOCAL_MODEL_PATH"]
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
model = OpenAIServerModel(
    model_id=LOCAL_MODEL_PATH,
    api_base=BASE_URL,  # Leave this blank to query OpenAI servers.
    api_key=API_KEY,  # Switch to the API key for the server you're targeting.
)

# Define MCP server parameters
weather_server_parameters = StdioServerParameters(
    command="uv",
    args=["run", "python", "/data/dong-qichang/codes/mcp-exercise/quick_starts/weather_forecast/weather.py"],
    env={"UV_PYTHON": "3.11", **os.environ},
)
pubme_server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

use_2_tools = False
if use_2_tools:
    # Load tools from MCP servers
    with ToolCollection.from_mcp(
        weather_server_parameters, trust_remote_code=True
    ) as weather_tool_collection, ToolCollection.from_mcp(
        pubme_server_parameters
    ) as pubme_tool_collection:
        all_tools = [*weather_tool_collection.tools, *pubme_tool_collection.tools]
        # Create an agent with all tools
        agent = CodeAgent(tools=all_tools, model=model, add_base_tools=True)
        # Visualize agent behavior
        agent.visualize()
        print(agent.run("weather in Los Angeles"))
        print(agent.run("pubmed search for covid"))
else:
    # Load tools from a single MCP server
    with ToolCollection.from_mcp(
        weather_server_parameters, trust_remote_code=True
    ) as weather_tool_collection:
        # Create an agent with all tools
        agent = CodeAgent(tools=weather_tool_collection.tools, model=model, add_base_tools=True)
        # Visualize agent behavior
        # agent.visualize()
        print(agent.run("weather in Shanghai"))