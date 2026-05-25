# LangGraph node functions.
#
# agent_node(state: AgentState) -> AgentState
#   - Initialises ChatAnthropic with the model from config
#   - Binds the four tools (check_availability, book_appointment,
#     list_appointments, cancel_appointment) to the model via .bind_tools()
#   - Calls the model with the current message history
#   - Returns the updated state with the new AIMessage appended
#
# should_continue(state: AgentState) -> Literal["tools", END]
#   - Conditional edge function
#   - If the last AIMessage contains tool_calls  → return "tools"
#   - Otherwise (final answer)                  → return END
#
# The ToolNode is imported from langgraph.prebuilt and wired in graph.py;
# no custom node function is needed for tool execution.
