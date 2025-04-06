from smolagents import OpenAIServerModel, CodeAgent, ActionStep, TaskStep
from dotenv import load_dotenv
import os
from loguru import logger


load_dotenv()
API_KEY = os.environ["API_KEY"]
LOCAL_MODEL_PATH = os.environ["LOCAL_MODEL_PATH"]
BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
logger.info(f'{LOCAL_MODEL_PATH = }')

model = OpenAIServerModel(
    model_id=LOCAL_MODEL_PATH,
    api_base=BASE_URL, # Leave this blank to query OpenAI servers.
    api_key=API_KEY, # Switch to the API key for the server you're targeting.
)


agent = CodeAgent(tools=[], model=model, verbosity_level=1, add_base_tools=True)
# print(agent.memory.system_prompt)

task = "What is the 20th Fibonacci number?"
# r = agent.run(task)
# logger.info(r)


# Let's start a new task!
logger.info('starting a new task')
agent.memory.steps.append(TaskStep(task=task, task_images=[]))
logger.info('starting a new loop')
final_answer = None
step_number = 1
while final_answer is None and step_number <= 10:
    memory_step = ActionStep(
        step_number=step_number,
        observations_images=[],
    )
    # Run one step.
    final_answer = agent.step(memory_step)
    agent.memory.steps.append(memory_step)
    step_number += 1

    # Change the memory as you please!
    # For instance to update the latest step:
    # agent.memory.steps[-1] = ...

print("The final answer is:", final_answer)