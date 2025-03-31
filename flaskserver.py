from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-python', methods=['POST'])
def run_python_script():
    data = request.get_json()
    model_file = data.get('modelFile')
    hash_value = data.get('hashValue')

    if not hash_value:
        return jsonify({'error': 'Missing hashValue'}), 400

    try:
        # Run Python script
        process = subprocess.Popen(
            ['python', 'rftest.py', model_file, hash_value],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = process.communicate()

        if process.returncode == 0:
            return jsonify({'result': output.decode().strip()})
        else:
            return jsonify({'error': error.decode().strip()}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
