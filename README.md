# Checklist+

## Description
Checklist+ is a dynamic to-do list application powered by an AI model to automatically generate useful tasks based on user prompts. It features a SQLite database for task storage, a Python-powered backend for functionality, and an HTML-based user interface for seamless interaction.

Soon to be published on AWS Lambda!

---

## Installation

Use these steps to download and install the project locally:

1. **Clone the Repository**:
   ```bash
   git clone <this-repository-url>
   cd <this-repository-folder>
   ```

2. **Set Up a Virtual Environment** (if modifying code - to sort and handle dependencies):
   ```bash
   python -m venv venv
   # On Linux: source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Environment Variables**:
   - Create a `.env` file in the same directory as your project.
   - Add the following line to the `.env` file:
     ```
     OPENAI_API_KEY=openai_api_key
     ```
     Replace `openai_api_key` with your OpenAI API key that you can generate on the openAI website.

5. **Initialize the Database**:
   - The application will automatically initialize the database (`checklist.db`) when you run it for the first time.
   - You can also manually create the database file by making a (`checklist.db`) file in the same directory as your project

6. **Run the Application**:
   ```bash
   python checklist.py
   ```

7. **Access the Web Interface**:
   - Go to `http://127.0.0.1:5000` on your web browser.

---

## Usage
Checklist+ has three ways to interact with your checklist list:

1. **Add a Task Manually**:
   - Use the input box labelled "Enter a new task" to type in your task.
   - Click the **Add Task** button to save it to the list.

2. **Delete a Task**:
   - Use the input box labelled "Enter the task number" to specify which task to delete.
   - The list deletes things by ID number and each item on the list has an ID starting from 1
   - Click the **Delete Task** button to remove it from the list.

3. **Generate Tasks with AI**:
   - Use the input box labelled "Enter a prompt" to describe a general idea or goal you want to accomplish.
   - Click the **Generate Tasks** button to receive a list of AI-generated tasks relevant to you which can help guide you.

4. **Clear All**:
    - This button will clear all the items on the list

---

## Technologies Used

- **Python**: Core language for the backend development.
- **Flask**: Used to handle route and the core web development.
- **SQLite**: This technology is used to store persistent data, it is a database software.
- **HTML & CSS**: Used for the frontend development and styling.
- **OpenAI API**: Used for the AI integration to generate tasks.
- **dotenv**: This is used to keep the API key used for testing secure and confidential.

---
