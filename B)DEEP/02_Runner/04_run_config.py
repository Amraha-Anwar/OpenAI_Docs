from agents import (
    Agent,
    Runner,
    RunConfig
)
from dotenv import load_dotenv

load_dotenv()

config = RunConfig(
    model = 'gpt-4o-mini'

    # 1- model: str | Model | None = None
    """The model to use for the entire agent run. If set, will override the model set on every
    agent. The model_provider passed in below must be able to resolve this model name.
    """

    # 2- model_provider: ModelProvider = field(default_factory=MultiProvider)
    """The model provider to use when looking up string model names. Defaults to OpenAI."""

    # 3- model_settings: ModelSettings | None = None
    """Configure global model settings. Any non-null values will override the agent-specific model
    settings.
    """

    # 4-  handoff_input_filter: HandoffInputFilter | None = None
    """A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that
    will take precedence. The input filter allows you to edit the inputs that are sent to the new
    agent. """

    # 5-  input_guardrails: list[InputGuardrail[Any]] | None = None
    """A list of input guardrails to run on the initial run input."""

    # 6-  output_guardrails: list[OutputGuardrail[Any]] | None = None
    """A list of output guardrails to run on the final output of the run."""

    # 7-  tracing_disabled: bool = False
    """Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.
    """

    # 8- trace_include_sensitive_data: bool = field( # default_factory=_default_trace_include_sensitive_data# )
    """Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or
    LLM generations) in traces. If False, we'll still create spans for these events, but the
    sensitive data will not be included.
    """

    # 9-  workflow_name: str = "Agent workflow"
    """The name of the run, used for tracing. Should be a logical name for the run, like
    "Code generation workflow" or "Customer support agent".
    """

    # 10- trace_id: str | None = None
    """A custom trace ID to use for tracing. If not provided, we will generate a new trace ID."""

    # 11- group_id: str | None = None
    """
    A grouping identifier to use for tracing, to link multiple traces from the same conversation
    or process. For example, you might use a chat thread ID.
    """

    # 12- trace_metadata: dict[str, Any] | None = None
    """
    An optional dictionary of additional metadata to include with the trace.
    """

    # 13- session_input_callback: SessionInputCallback | None = None
    """Defines how to handle session history when new input is provided.
    - `None` (default): The new input is appended to the session history.
    - `SessionInputCallback`: A custom function that receives the history and new input, and
      returns the desired combined list of items.
    """

    # 14- call_model_input_filter: CallModelInputFilter | None = None
    """
    Optional callback that is invoked immediately before calling the model. It receives the current
    agent, context and the model input (instructions and input items), and must return a possibly
    modified `ModelInputData` to use for the model call.

    This allows you to edit the input sent to the model e.g. to stay within a token limit.
    For example, you can use this to add a system prompt to the input.
    """
)

agent = Agent(
    name = "Assistant Agent",
    instructions = "You help user solve their problems.",
)

result = Runner.run_sync(
    agent,
    "hello",
    run_config = config
)

print(result.final_output)