import csv
import os
from langchain_community.document_loaders import WebBaseLoader
from bs4 import  SoupStrainer
import re

csvPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data.csv'))

def read_csv():
    with open(csvPath, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        return [{'id': row[0], 'url': row[1]} for row in reader]

def clean_text(text):
    text = re.sub(r'\n{2,}', '\n', text)
    text = '\n'.join([line.strip() for line in text.split('\n')])
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def fetch_data():
    docs = []
    for doc_info in read_csv():
        url = doc_info["url"]
        id = doc_info["id"]
        try:
            loader = WebBaseLoader(
                web_paths=[url],
                bs_kwargs={
                    "parse_only": SoupStrainer(["main","head"]) # Use SoupStrainer directly
                }
            )
            document = loader.load()
            if document:
                content = document[0].page_content
                cleaned_content = clean_text(content)
                docs.append({"id":id, "url":url,"page_content":cleaned_content})
        except Exception as e:
            print(f"Error loading or processing {url}: {e}")
    return docs

print(fetch_data())