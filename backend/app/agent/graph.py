# LangGraph graph definition.
#
# build_graph() -> CompiledGraph
#   Assembles and compiles the ReAct agent graph. Called once at startup.
#
# Graph topology:
#   START → agent_node
#   agent_node --[should_continue]--> tools_node  (if tool_calls present)
#   agent_node --[should_continue]--> END          (if final answer)
#   tools_node → agent_node
#
# Checkpointer:
#   - Development : MemorySaver (in-process, lost on restart)
#   - Production  : AsyncPostgresSaver (persistent, replace MemorySaver here)
#
# The compiled graph is stored on app.state.graph during the FastAPI lifespan
# so it is shared across all requests without recompilation.
