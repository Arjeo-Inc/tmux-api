# TMUX API


This project is a simple Flask application that provides a RESTful API for executing tmux commands. It's set up to run within a Docker container.


## Running the Application

To run this application, you need to have Docker installed on your machine. Follow the instructions below:

1. Build the Docker image:
2. Run the Docker container: 
## API Usage
Once the application is running, you can send a POST request to the  endpoint with a JSON body containing the tmux command to be executed. The command should come in under the key 'command'.
Example Curl command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"role": "system", "content": "tmux new-session -d"}' http://localhost:5000/v1/chat/completions
```
This Curl command sends a POST request to the `/v1/chat/completions` endpoint to create a new tmux session.

Example Curl command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"role": "system", "content": "tmux list-sessions"}' http://localhost:5000/v1/chat/completions
```
This Curl command sends a POST request to the `/v1/chat/completions` endpoint to list the tmux sessions.
