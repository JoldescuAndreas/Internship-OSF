from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

# Sample data - In a real application, you would use a database to store tasks.
tasks = {
    1: {"title": "Task 1", "description": "Description for Task 1"},
    2: {"title": "Task 2", "description": "Description for Task 2"},
}

# Helper function to abort if task not found
def abort_if_task_not_found(task_id):
    if task_id not in tasks:
        abort(404, message="Task not found")

# Request parser for POST and PUT requests
task_parser = reqparse.RequestParser()
task_parser.add_argument("title", type=str, required=True, help="Title of the task is required.")
task_parser.add_argument("description", type=str, required=True, help="Description of the task is required.")

# Resource for handling all tasks and creating a new task
class TaskListResource(Resource):
    def get(self):
        return tasks, 200

    def post(self):
        args = task_parser.parse_args()
        task_id = max(tasks.keys()) + 1
        tasks[task_id] = {"title": args["title"], "description": args["description"]}
        return tasks[task_id], 201

# Resource for handling a specific task
class TaskResource(Resource):
    def get(self, task_id):
        abort_if_task_not_found(task_id)
        return tasks[task_id], 200

    def put(self, task_id):
        abort_if_task_not_found(task_id)
        args = task_parser.parse_args()
        tasks[task_id]["title"] = args["title"]
        tasks[task_id]["description"] = args["description"]
        return tasks[task_id], 200

    def delete(self, task_id):
        abort_if_task_not_found(task_id)
        deleted_task = tasks.pop(task_id)
        return deleted_task, 200

# Register the resources with the API
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
