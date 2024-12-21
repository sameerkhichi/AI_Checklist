#This is the import statement for the Flask app that allows me to build the web application
from flask import Flask

#the  __name__ operator is a special variable in python
#it stores the name of the file that is currently being executed
checklist = Flask(__name__) #creating an instance of the flask class

#this route calls the home function when the user visits the root of the URL
@checklist.route('/')
def home():
    return ("This is the web framework for the AI checklist")

if __name__ == '__main__':
    checklist.run(debug=True) #flask development server, listens for request from URL


#This file creates a localhost or local server 