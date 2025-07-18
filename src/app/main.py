import pathlib
from fastapi import FastAPI
from pydantic import BaseModel
from src.llm.generate_answer import ask_question
from src.processing.process_csv import process_csv
from src.llm import generate_answer
app = FastAPI()
generate_answer.setup_qa_chain()
class questionreq(BaseModel):
    question:str

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

@app.get("/delete_local_index")
async def delete_local_index():
    """
    Deletes all files within the specified local index folder.
    """
    # Use pathlib.Path for object-oriented filesystem paths
    index_folder_path = pathlib.Path("data/faiss_index")

    # Check if the directory exists to avoid errors
    if not index_folder_path.exists():
        print(f"Directory not found: {index_folder_path}")
        return

    print(f"Clearing files in: {index_folder_path}")
    # Iterate through all entries in the directory
    for entry in index_folder_path.iterdir():
        try:
            # Check if the entry is a file before deleting
            if entry.is_file():
                print(f"Deleting file: {entry.name}")
                entry.unlink()
        except Exception as e:
            print(f"Error deleting {entry.name}: {e}")

# def test():
#     return "I can execute"
# if __name__ == "__main__":
