from fastapi import FastAPI
from pydantic import BaseModel
# from src.llm.generate_answer import ask_question
# from src.processing.process_csv import process_csv
app = FastAPI()
def start_application():
    class questionreq(BaseModel):
        question:str
    @app.get("/")
    def read_root():
        """A root endpoint to confirm the API is running."""
        return {"message": "API is running. Send POST requests to /question."}

    @app.post("/question")
    async def ask_question(request_data: questionreq):
        """Receives a question and returns a placeholder answer."""
        answer = f"This is a placeholder answer for: '{request_data.question}'"
        return {"answer": answer}

    # @app.post("/question")
    # async def answer(q: questionreq):
    #     answer = ask_question(q.question)
    # return {"answer":answer}
    
    # @app.post("/question")
    # async def process_csv():
    #     answer = process_csv()
    # return {"Result":answer}

def test():
    return "I can execute"
if __name__ == "__main__":
    start_application()
