# TMUX API


This project is a simple Flask application that provides a RESTful API for executing tmux commands. It's set up to run within a Docker container.


## Running the Application

To run this application, you need to have Docker installed on your machine. Follow the instructions below:

1. Build the Docker image:
2. Run the Docker container: 
## API Usage
Once the application is running, you can send a POST request to the  endpoint with a JSON body containing the tmux command to be executed. The command should come in under the key 'command'.
Example Curl command:
{"response":"0: 1 windows (created Wed Feb 14 22:54:44 2024)
"}
This Curl command sends a POST request to the  endpoint to list the tmux sessions.
