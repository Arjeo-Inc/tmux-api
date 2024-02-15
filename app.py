from flask import Flask, request, jsonify, after_this_request
import subprocess
import shlex  # Importing shlex to safely split the command string into a list

app = Flask(__name__)

@app.route('/')
def root():
    return "Flask application is running!"

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def openai_command():
    #response = jsonify({"data":[{"id":"tmux","object":"model","created":1677610602,"owned_by":"openai"}],"object":"list"})
    response = app.response_class()
    if request.method == 'OPTIONS':
        return response

    data = request.get_json(force=True, silent=True)
    if not data:
        response = jsonify({'error': 'Invalid JSON'})
        response.status_code = 400
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    messages = data.get('messages')
    if not messages:
        response = jsonify({'error': 'No messages provided'})
        response.status_code = 400
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    command_str = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), None)
    if not command_str:
        response = jsonify({'error': 'No command specified'})
        response.status_code = 400
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # Use shlex to safely split the command string into a list
    # This is important to correctly process commands with spaces, quotes, etc.
    command_list = shlex.split(command_str)

    # Ensure the command is prefixed with 'tmux' to maintain the scope of this API
    # This is a basic check and might need to be more sophisticated for real-world applications
    if not command_list or command_list[0] != 'tmux':
        response = jsonify({'error': 'Invalid command'})
        response.status_code = 400
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    def generate():
        import json
        try:
            output = subprocess.check_output(command_list, stderr=subprocess.STDOUT)
            yield 'data: %s\n\n' % json.dumps({"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1694268190, "model": "gpt-3.5-turbo-0613", "system_fingerprint": "fp_44709d6fcb", "choices": [{"index": 0, "delta": {"role": "assistant", "content": output.decode('utf-8')}, "logprobs": None, "finish_reason": None}]})
        except subprocess.CalledProcessError as e:
            yield 'data: %s\n\n' % json.dumps({"id": "chatcmpl-123", "object": "chat.completion.chunk", "created": 1694268190, "model": "gpt-3.5-turbo-0613", "system_fingerprint": "fp_44709d6fcb", "choices": [{"index": 0, "delta": {"role": "assistant", "content": "Command failed: " + e.output.decode('utf-8')}, "logprobs": None, "finish_reason": None}]})
    response = app.response_class(generate(), mimetype='text/event-stream')
    return response

@app.route('/v1/models', methods=['GET', 'OPTIONS'])
def get_models():
    response = jsonify({"data":[{"id":"tmux","object":"model","created":1677610602,"owned_by":"openai"}],"object":"list"})
    return response

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
