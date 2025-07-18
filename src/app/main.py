from fastapi import FastAPI
from pydantic import BaseModel
from src.llm.generate_answer import ask_question
from src.processing.process_csv import process_csv
from src.llm import generate_answer
app = FastAPI()
generate_answer.setup_qa_chain()
class questionreq(BaseModel):
    question:str
@app.get("/")
def read_root():
    """A root endpoint to confirm the API is running."""
    return {"message": "API is running. Send POST requests to /question."}

@app.post("/question")
def ask(request_data: questionreq):
    """Receives a question and returns a placeholder answer."""
    answer = ask_question(request_data.question)
    return answer

@app.get("/process_csv_file")
async def process_csv_file():
    """Receives a question and returns a placeholder answer."""
    process_csv()
    return {}

# def test():
#     return "I can execute"
# if __name__ == "__main__":
