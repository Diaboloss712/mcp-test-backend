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

'''
프롬프트 예시 
{
  "prompt": "I need you to make the question for an examination. 
  The subject is Computer Science and the topic is Computer Network. 
  You can freely decide the contents and the subtopic of the question freely. 
  For more information check the system prompt and example json format. 
  The type of the question if either 'select' or 'write'. 
  Also, the category of the question should be consist of subject, topic, and subtopic in form Subject/Topic/Subtopic (put slash '/' between each classification). 
  Which means you CANNOT use slash(/) for a single category such as 'TCP/IP'. 
  Please keep in mind that your reponse must be returned in json format!! No matter what!!"
}
'''