FROM python:3.12-slim


RUN pip install --no-cache-dir \
    mcpo>=0.0.17 \
    fastmcp>=0.1.2 \
    requests>=2.31.0


COPY src/* /app/
WORKDIR /app

ENV MCPO_API_KEY=""

ENV JIRA_BASE_URL=""
ENV JIRA_PAT=""
ENV CONFLUENCE_BASE_URL=""
ENV CONFLUENCE_PAT=""

EXPOSE 8000

# Start MCPO and run the MCP server over stdio
# MCPO will serve OpenAPI at /docs and require the API key
CMD mcpo --port 8000 --api-key "$MCPO_API_KEY" -- python /app/confluence_mcp_server.py
