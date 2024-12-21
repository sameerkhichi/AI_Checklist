#this document is overcommented for learning purposes
#This is the import statement for the Flask app that allows me to build the web application
import sqlite3
from flask import Flask, request, jsonify

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

initialize_database()


#this root is called to add a task when the user interacts with the root URL
@checklist.route('/add_task', methods = ['POST'])
def add_task():
    data = request.json #fetching the information from the request 
    #this will get the data from task
    task = data.get('task')

    if task: #if there was a task provided then add it to the temporary storage
        
        connection = sqlite3.connect("checklist.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))

        #closing the connection to the database
        connection.commit()
        connection.close()

        return jsonify({"message": "Added the task to the list!"}), 201
    return jsonify({"error": "A task is required to add something to the list"}), 400
        

#this route will delete the task from the list
@checklist.route('/delete_task', methods = ['DELETE'])
def delete_task():

    #fetch the data of the task in question 
    data = request.json
    task_id = data.get('id')

    #remove the task based off of its id
    if task_id:
        connection = sqlite3.connect("checklist.db")
        cursor = connection.cursor()

        #remove the task
        cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))

        connection.commit()
        connection.close()
        
        return jsonify({"message": "Deleted the task"}), 200
    
    #incase the task is not in the current list, print and error message.
    return jsonify({"error": "A task is required to remove something to the list"}), 404

#this route just gets the tasks using the HTTP method GET
@checklist.route('/read_task', methods = ['GET'])
def read_task():

    connection = sqlite3.connect("checklist.db")
    cursor = connection.cursor()

    #grab all the tasks from the database file
    cursor.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]

    connection.close()

    return jsonify({"tasks":tasks})


if __name__ == '__main__':
    checklist.run(debug=True) #flask development server, listens for request from URL


#This file creates a localhost or local server 