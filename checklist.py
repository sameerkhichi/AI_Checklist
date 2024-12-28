#this document is overcommented for learning purposes
#This is the import statement for the Flask app that allows me to build the web application
#note that a migration tool was used to update the openAI model version.
import os
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for

#loading the environment variables to make API calls to openai
load_dotenv()

#declaring the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#the  __name__ operator is a special variable in python
#it stores the name of the file that is currently being executed
checklist = Flask(__name__) #creating an instance of the flask class


def initialize_database():

    #these lines of code connects to the database
    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    #creating the tasks table if there isnt one there
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()

#a function to reorder the tags of the ids to make them countable
def reorder_id_tags():

    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    #getting all the tasks as a tuple from the database
    cursor.execute("SELECT id, task FROM tasks ORDER BY id")
    tasks = cursor.fetchall()


    dynamic_id = 1

    #making sure the for loop supports type tuple 
    for set_id, task in tasks:
        #replaces the old id with a new one counting starting from one
        cursor.execute("UPDATE tasks SET id = ? WHERE id = ?", (dynamic_id, set_id))
        dynamic_id += 1

    connection.commit()
    connection.close()

#This essentailly starts the database
initialize_database()

#this function is made for code simplicity
#used to insert any tasks to the database
def inserting_to_database(task):

    #connect to the database
    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    #if there is a task then add it to the database
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))

    #commit and close the connection to the database
    connection.commit()
    connection.close()


#an endpoint to create tasks with a general prompt
@checklist.route('/generate_tasks', methods = ['POST'])
def generate_tasks():

    general_request = request.form.get('general_request')

    response = client.chat.completions.create(model = "gpt-3.5-turbo",
    
    #initializing the model, its role and what it has to do
    messages = [
        {"role": "system", "content": "you are a values assistant tasked with creating meaningful tasks to add to a to-do list based on a user request."},
        {"role": "user", "content": f"Generate a meaningful list of tasks based on this request seperate them using new line characters: {general_request}"}
    ])

    #extracts the response by using the content in the first index of the choices given in the object returned by the model
    model_response = response.choices[0].message.content

    #the tasks are given in the response seperated by new line characters
    tasks = model_response.split("\n")

    for task in tasks: #insert tasks given by the model to the database
        inserting_to_database(task)

    return redirect(url_for('web_interface'))

#this root is called to add a task when the user interacts with the root URL
@checklist.route('/add_task', methods = ['POST'])
def add_task():
    #data = request.json #fetching the information from the request 
    #this will get the data from task
    #task = data.get('task')

    #instead of getting data of type json getting it in the form for HTML
    task = request.form.get('task')

    inserting_to_database(task)

    #redirect user to home root after adding a task instead of using a json return
    #url_for is the url for the function provided, and redirect takes user there
    return redirect(url_for('web_interface')) #hardcode = redirect('/')


#this route will delete the task from the list
@checklist.route('/delete_task', methods = ['POST'])
def delete_task():

    #fetch the data of the task in question 
    #data = request.json
    #task_id = data.get('id')

    #getting the task ID in the form for HTML
    task_id = request.form.get("task_id")

    #remove the task based off of its id
    if task_id:
        connection = sqlite3.connect("checklist.db")
        cursor = connection.cursor()

        #remove the task
        cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))

        connection.commit()
        connection.close()

        #reorder the tags after having deleted something
        reorder_id_tags()

        #redirecting to the home root
        return redirect(url_for('web_interface'))
    return redirect(url_for('web_interface'))

#this route just gets the tasks using the HTTP method GET
@checklist.route('/read_task', methods = ['GET'])
def read_task():

    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    #grab all the tasks from the database file
    cursor.execute("SELECT * FROM tasks")

    #note that fetchall returns a list where each element has an ID, these are all rows of the database
    #row[0] gets the id column and row[1] gets the tasks column
    tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]

    connection.close()

    return jsonify({"tasks":tasks})

#making a route for the front end part of the webpage 
# / makes it so it triggers as soon as someone visits the base URL
@checklist.route('/')
def web_interface():

    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]

    connection.close()

    #linked to the file where the html code is stored 
    return render_template("web_interface.html", tasks = tasks)




if __name__ == '__main__':
    checklist.run(debug=True) #flask development server, listens for request from URL


#This file creates a localhost or local server 