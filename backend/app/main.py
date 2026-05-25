# FastAPI application entry point.
#
# Responsibilities:
#   - Create the FastAPI app instance
#   - Register the lifespan context (compile the LangGraph graph once at startup)
#   - Mount CORSMiddleware allowing localhost:4200 (client-app) and localhost:4201 (admin-app)
#   - Include routers: api/routes/chat.py and api/routes/appointments.py
#   - Expose a simple GET /health endpoint
