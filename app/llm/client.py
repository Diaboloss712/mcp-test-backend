import asyncio
import httpx

MCP_SERVER_URL = "http://localhost:11500/call"  # FastMCP SSE 서버 주소

async def call_llm_generate_problem(prompt: str) -> dict:
    """
    FastMCP SSE 서버에 prompt를 전달하여 문제 데이터를 받아옵니다.
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            MCP_SERVER_URL,
            json={
                "tool": "generate_problem",
                "input": {"prompt": prompt}
            },
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()["output"]

