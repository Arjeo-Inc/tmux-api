import requests
import json
import time
import subprocess

def test_app():
    # Launch a new tmux session in detached mode
    data = {"role": "system", "content": "tmux new-session -d"}
    response = requests.post('http://localhost:5000/openai', json=data)
    print(response.text)

    time.sleep(1)  # Wait for the tmux session to be ready

    # Execute the 'ls /' command
    data = {"role": "system", "content": "tmux send-keys 'ls /' Enter"}
    response = requests.post('http://localhost:5000/openai', json=data)
    print(response.text)

    time.sleep(1)  # Wait for the command to execute

    # Capture the output
    data = {"role": "system", "content": "tmux capture-pane -p"}
    response = requests.post('http://localhost:5000/openai', json=data)
    print(response.text)

if __name__ == '__main__':
    # Start the Flask application in a new process
    flask_process = subprocess.Popen(['flask', 'run'])
    try:
        test_app()
    finally:
        # Stop the Flask application
        flask_process.terminate()
