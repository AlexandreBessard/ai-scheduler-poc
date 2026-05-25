# LangGraph agent state definition.
#
# AgentState is a TypedDict that represents the data flowing through the graph.
#
# Fields:
#   - messages: Annotated[list[BaseMessage], add_messages]
#       Conversation history (HumanMessage, AIMessage, ToolMessage).
#       The add_messages reducer appends new messages rather than overwriting.
#   - thread_id: str
#       Passed through for reference; the actual checkpointing key is set
#       in the graph config, not in the state itself.
#
# This state is initialised per conversation turn and persisted between turns
# by the LangGraph checkpointer (MemorySaver in dev, AsyncPostgresSaver in prod).
