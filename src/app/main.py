# from fastapi import FastAPI

# app = FastAPI()


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from src.llm.generate_answer import ask_question

# @app.get("/question/{question}")
# async def read_question(question: str):
#      answer = ask_question(question)
#      return answer
from fastapi import FastAPI
from pydantic import BaseModel
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.llm.generate_answer import ask_question

app = FastAPI()

class questionreq(BaseModel):
    question:str

@app.post("/question")
async def answer(q: questionreq):
    answer = ask_question(q.question)
    return {"answer":answer}

# def main():
#     while True:
#         query = input("Ask me anything: ")
#         answer = ask_question(query)
#         print(f"\n💡 {answer}\n")

# if __name__ == "__main__":
#     main()
