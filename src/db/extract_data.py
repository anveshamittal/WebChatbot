import pyodbc
import os

def fetch_data():
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=DESKTOP-VAR056C\\SQLEXPRESS;Database=mydatabase;UID=sa;PWD=A1m13i9t20@@;TrustServerCertificate=Yes;")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()
    return [{"title": r.ProductName, "body": r.UnitPrice, "url": r.UnitsOnOrder} for r in rows]
 
docs=fetch_data()
