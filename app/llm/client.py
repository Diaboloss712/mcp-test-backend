import asyncio
import httpx

MCP_SERVER_URL = "http://localhost:11500/call"  # FastMCP 서버 주소

async def call_llm_generate_problem(prompt: str, llm: str = "hyperclova") -> dict:
    """
    MCP 서버에 prompt와 원하는 LLM을 전달하여 문제 데이터를 받아옵니다.
    
    Parameters:
    - prompt (str): 문제 생성 요청 프롬프트
    - llm (str): 사용할 LLM 이름 ('ollama', 'chatgpt', 'hyperclova')

    Returns:
    - dict: 생성된 문제 정보
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            MCP_SERVER_URL,
            json={
                "tool": "generate_problem",
                "input": {
                    "prompt": prompt,
                    "llm": llm
                }
            },
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()["output"]

# 사용 예시
if __name__ == "__main__":
    prompt_text = "Create a multiple choice question about deep learning optimizers."
    llm_name = "ollama"  # 또는 "chatgpt", "hyperclova"

    result = asyncio.run(call_llm_generate_problem(prompt_text, llm=llm_name))
    print(result)


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