# Understanding the concept of **MAX_TURNS**


## The Flow of **TURNS with Tool**


### Turn 1: **The Reasoning Turn**


*STEP1*: The user provides a query to the agent.  

*Step2*: The agent sends the user's query and a list of available tools to the LLM.    

*Step3*: The LLM's output, based on its internal reasoning, is to choose a tool and specify the arguments to call it with. The LLM doesn't give a final answer yet because it needs the tool's result.  


### Turn 2: **The Acting and Finalizing Turn**


*Step1*: The agent receives the LLM's instruction and executes the tool call.  

*Step2*: The tool returns a result (e.g., "The weather is 25 degrees Celsius").  

*Step3*: The agent takes the original query, the LLM's previous reasoning, and the new tool output and sends it all back to the LLM.  

*Step4(LLM's Final Answer)* : The LLM now has all the information it needs. It processes the tool output and formulates the final, human-readable response. The agent then provides this to the user.  

---

