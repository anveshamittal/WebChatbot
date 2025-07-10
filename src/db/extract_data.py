import pyodbc
import os

def fetch_data():
    conn = pyodbc.connect(os.getenv("SQL_CONNECTION_STRING"))
    cursor = conn.cursor()
    cursor.execute("SELECT Title, Body, Url FROM ContentTable WHERE Published = 1")
    rows = cursor.fetchall()
    return [{"title": r.Title, "body": r.Body, "url": r.Url} for r in rows]