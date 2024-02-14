from flask import Flask, request, jsonify
import subprocess
import shlex  # Importing shlex to safely split the command string into a list

app = Flask(__name__)

@app.route('/tmux', methods=['POST'])
def tmux_command():
    data = request.json
    command_str = data.get('command')
    if not command_str:
        return jsonify({'error': 'No command specified'}), 400

    # Use shlex to safely split the command string into a list
    # This is important to correctly process commands with spaces, quotes, etc.
    command_list = shlex.split(command_str)

    # Ensure the command is prefixed with 'tmux' to maintain the scope of this API
    # This is a basic check and might need to be more sophisticated for real-world applications
    if not command_list or command_list[0] != 'tmux':
        return jsonify({'error': 'Invalid command'}), 400

    try:
        # Execute the tmux command and get output
        # Now passing a list to subprocess.check_output to handle commands with flags/arguments
        output = subprocess.check_output(command_list, stderr=subprocess.STDOUT)
        return jsonify({'response': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Command failed', 'details': e.output.decode('utf-8')}), 400

if __name__ == '__main__':
    app.run(debug=True)
