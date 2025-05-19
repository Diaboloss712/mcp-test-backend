# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_generate_problem_from_prompt():
#     payload = {
#         "prompt": "TCP의 3-way handshake에 대해 설명하는 문제를 생성해줘."
#     }
#     response = client.post("/problems/generate", json=payload)

#     assert response.status_code == 200
#     assert "title" in response.json()
#     assert "content" in response.json()
#     assert "category" in response.json()