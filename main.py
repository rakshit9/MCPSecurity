from fastapi import FastAPI
from config.settings import settings
from mcp_server.routes import router as guardrails_router
from mcp_server.opa_routes import router as opa_router
import uvicorn

app = FastAPI(
    title="MCPSecurity Gateway",
    description="Secure MCP Gateway with Bidirectional Security - Enterprise LLM Protection",
    version="0.1.0"
)

app.include_router(guardrails_router)
app.include_router(opa_router)


@app.get("/")
async def root():
    return {
        "service": "MCPSecurity Gateway",
        "status": "running",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "input_guardrails": "enabled",
            "opa_policies": "enabled",
            "output_guardrails": "pending",
            "static_analysis": "pending",
            "langgraph_agents": "pending"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.MCP_SERVER_HOST,
        port=settings.MCP_SERVER_PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )

