# Understanding the concept of **MAX_TURNS**


## The Flow of **TURNS with Tool**


### Turn 1: **The Reasoning Turn**


- *STEP1*: The user provides a query to the agent.  

- *STEP2*: The agent sends the user's query and a list of available tools to the LLM.    

- *STEP3*: The LLM's output, based on its internal reasoning, is to choose a tool and specify the arguments to call it with. The LLM doesn't give a final answer yet because it needs the tool's result.  


### Turn 2: **The Acting and Finalizing Turn**


- *STEP1*: The agent receives the LLM's instruction and executes the tool call.  

- *STEP2*: The tool returns a result (e.g., "The weather is 25 degrees Celsius").  

- *STEP3*: The agent takes the original query, the LLM's previous reasoning, and the new tool output and sends it all back to the LLM.  

- *STEP4(LLM's Final Answer)* : The LLM now has all the information it needs. It processes the tool output and formulates the final, human-readable response. The agent then provides this to the user.    

<br>

📌 By setting  `tool_use_behavior = 'stop_on_first_tool'` we can run an agent with a tool in a single turn  
Similarly, with the sub-agent (handoff) concept, we can pass sub-agents as `agents as tools` and apply the same tool_use_behavior setting.

<br>

---  
  
<br>


# **tool_choice** VS **is_enabled**

<br>

## is_enabled = False, tool_choice = 'required' 


```python
from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import random

load_dotenv()

@function_tool(is_enabled = False)
def random_number(num1: int, num2: int)-> str:
    """generates random number
    
    Arg
        num1: the frst number from which the limit starts
        num2: the last limit number 
    """
    return f"The random number I've chosen for you is 🔢{random.randint(num1, num2)}🔢"

agent = Agent(
    name = "number generator",
    instructions = "you are a mathematician. If user asks you to choose any random number, you must have to use the tool"
    "If the tool is not available, do apologies but Don't respond by yourself.",
    model = 'gpt-4o-mini',
    tools = [random_number],
    model_settings = ModelSettings(
        tool_choice = 'required'
    )
)

response = Runner.run_sync(
    agent,
    "I'm confused, choose a random number for me between 1 - 10."
)

print(response.final_output)
```

### **Output:** <br>
`openai.BadRequestError: Error code: 400`

<br>

📌 This error occurs when the model is explicitly instructed to use a tool via `(tool_choice = 'required')`, but the tool itself is disabled `(is_enabled = False)`. The request fails because it creates a logical contradiction: the model is required to use a tool that is not available to it.

<br>
<br>

---

## is_enabled = True , tool_choice = 'none'


```python
from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
import random

load_dotenv()

@function_tool(is_enabled = True)
def random_number(num1: int, num2: int)-> str:
    """generates random number
    
    Arg
        num1: the frst number from which the limit starts
        num2: the last limit number 
    """
    return f"The random number I've chosen for you is 🔢{random.randint(num1, num2)}🔢"

agent = Agent(
    name = "number generator",
    instructions = "you are a mathematician. If user asks you to choose any random number, you must have to use the tool"
    "If the tool is not available, do apologies but Don't respond by yourself.",
    model = 'gpt-4o-mini',
    tools = [random_number],
    model_settings = ModelSettings(
        tool_choice = 'none'
    )
)

response = Runner.run_sync(
    agent,
    "I'm confused, choose a random number for me between 1 - 10."
)

print(response.final_output)
```

### **Output:** <br>
`I'm unable to select a random number at the moment. Please try again later!`

<br>

📌 This response is generated when a tool is enabled `(is_enabled = True)` but the model is explicitly forbidden from using it `(tool_choice = 'none')`. The model, adhering to its instructions, cannot call the tool and instead produces a pre-defined, apologetic response.

<br>
<br>

---

