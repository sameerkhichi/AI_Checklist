#this document is overcommented for learning purposes
#This is the import statement for the Flask app that allows me to build the web application
from flask import Flask, request, jsonify

#the  __name__ operator is a special variable in python
#it stores the name of the file that is currently being executed
checklist = Flask(__name__) #creating an instance of the flask class

#this is a temporary storage device containing the tasks on the list 
tasks = []

#this root is called to add a task when the user interacts with the root URL
@checklist.route('/add_task', methods = ['POST'])
def add_task():
    data = request.json #fetching the information from the request 
    #this will get the data from task
    task = data.get('task')

    if task: #if there was a task provided then add it to the temporary storage
        tasks.append(task)
        return jsonify({"message": "Added the task to the list!", "tasks": tasks}), 201
    return jsonify({"error": "A task is required to add something to the list"}), 400
        

#this route will delete the task from the list
@checklist.route('/delete_task', methods = ['DELETE'])
def delete_task():

    #fetch the data of the task in question 
    data = request.json
    task = data.get('task')

    #if the task is in the list then remove it
    if task in tasks:
        tasks.remove(task)
        return jsonify({"message": "Deleted the task", "tasks": tasks}), 200
    return jsonify({"error": "A task is required to remove something to the list"}), 404

#this route just gets the tasks using the HTTP method GET
@checklist.route('/read_task', methods = ['GET'])
def read_task():
    return jsonify({"tasks":tasks})


if __name__ == '__main__':
    checklist.run(debug=True) #flask development server, listens for request from URL


#This file creates a localhost or local server 