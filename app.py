from flask import Flask, request, jsonify
import subprocess
import shlex  # Importing shlex to safely split the command string into a list

app = Flask(__name__)

@app.route('/')
def root():
    return "Flask application is running!"

@app.route('/v1/chat/completions', methods=['POST'])
def openai_command():
    data = request.json
    messages = data.get('messages')
    command_str = [msg['content'] for msg in messages if msg['role'] == 'user'][0]
    if not command_str:
        return jsonify({'error': 'No command specified'}), 400

    # Use shlex to safely split the command string into a list
    # This is important to correctly process commands with spaces, quotes, etc.
    command_list = shlex.split(command_str)

    # Ensure the command is prefixed with 'tmux' to maintain the scope of this API
    # This is a basic check and might need to be more sophisticated for real-world applications
    if not command_list or command_list[0] != 'tmux':
        return jsonify({'error': 'Invalid command'}), 400

    def generate():
        try:
            # Execute the tmux command and get output
            # Now passing a list to subprocess.check_output to handle commands with flags/arguments
            output = subprocess.check_output(command_list, stderr=subprocess.STDOUT)
            yield 'data: {"id": "any_id", "object": "text.completion", "created": 0, "model": "gpt-3.5-turbo", "choices": [{"text": "' + output.decode('utf-8') + '", "finish_reason": "stop", "index": 0}]}\n\n'
        except subprocess.CalledProcessError as e:
            yield 'data: {"id": "any_id", "object": "text.completion", "created": 0, "model": "gpt-3.5-turbo", "choices": [{"text": "Command failed: ' + e.output.decode('utf-8') + '", "finish_reason": "stop", "index": 0}]}\n\n'
    return app.response_class(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
