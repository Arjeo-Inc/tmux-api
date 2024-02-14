from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/tmux', methods=['POST'])
def tmux_command():
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({'error': 'No command specified'}), 400
    try:
        # Execute the tmux command and get output
        output = subprocess.check_output(['tmux', command], stderr=subprocess.STDOUT)
        return jsonify({'response': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Command failed', 'details': e.output.decode('utf-8')}), 400

if __name__ == '__main__':
    app.run(debug=True)
