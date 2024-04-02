from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

from flask import Flask, render_template, request
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

##

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form.get("question")
        if question.strip() != "":
            response = get_gemini_response(question,prompt)
            if response:
                result_rows = read_sql_query(response, "student.db")
                if len(result_rows) > 0:
                    return render_template("results.html", rows=result_rows)
                else:
                    return "No results found."
            else:
                return "Invalid query or no response received."
        else:
            return "Please enter a SQL query."
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)









