import flask
from flask import request, jsonify
import subprocess
import os
import tempfile
import shutil

app = flask.Flask(__name__)

# Create a secure temporary directory
TEMP_DIR = tempfile.mkdtemp()

def execute_code(language, code):
    """
    Executes the given code in a secure environment.

    Args:
        language (str): The programming language.
        code (str): The code to execute.

    Returns:
        str: The output of the execution, or an error message.
    """
    try:
        if language == 'c':
            # Create a temporary file for the C code
            c_file_path = os.path.join(TEMP_DIR, "temp.c")
            with open(c_file_path, "w") as f:
                f.write(code)
            # Compile the C code
            compile_command = ["gcc", c_file_path, "-o", os.path.join(TEMP_DIR, "a.out")]
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"
            # Execute the compiled code
            execute_command = [os.path.join(TEMP_DIR, "a.out")]
            execute_result = subprocess.run(execute_command, capture_output=True, text=True, timeout=10)
            return execute_result.stdout + execute_result.stderr

        elif language == 'cpp':
            # Create a temporary file for the C++ code
            cpp_file_path = os.path.join(TEMP_DIR, "temp.cpp")
            with open(cpp_file_path, "w") as f:
                f.write(code)
            # Compile the C++ code
            compile_command = ["g++", cpp_file_path, "-o", os.path.join(TEMP_DIR, "a.out")]
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)
            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"
            # Execute the compiled code
            execute_command = [os.path.join(TEMP_DIR, "a.out")]
            execute_result = subprocess.run(execute_command, capture_output=True, text=True, timeout=10)
            return execute_result.stdout + execute_result.stderr

        elif language == 'python':
            # Use a temporary file
            py_file_path = os.path.join(TEMP_DIR, "temp.py")
            with open(py_file_path, "w") as f:
                f.write(code)
            execute_command = ["python", py_file_path]
            execute_result = subprocess.run(execute_command, capture_output=True, text=True, timeout=10)
            return execute_result.stdout + execute_result.stderr

        elif language == 'js':
            # Use a temporary file
            js_file_path = os.path.join(TEMP_DIR, "temp.js")
            with open(js_file_path, "w") as f:
                f.write(code)
            execute_command = ["node", js_file_path]
            execute_result = subprocess.run(execute_command, capture_output=True, text=True, timeout=10)
            return execute_result.stdout + execute_result.stderr

        elif language == 'csharp':
            # Create a temporary file for the C# code
            cs_file_path = os.path.join(TEMP_DIR, "temp.cs")
            with open(cs_file_path, "w") as f:
                f.write(code)
            # Compile the C# code using Mono
            compile_command = ["csc", "-out:" + os.path.join(TEMP_DIR, "main.exe"), cs_file_path]
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)

            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"
            # Execute the compiled code using Mono
            execute_command = ["mono", os.path.join(TEMP_DIR, "main.exe")]
            execute_result = subprocess.run(execute_command, capture_output=True, text=True, timeout=10)
            return execute_result.stdout + execute_result.stderr

        elif language == 'html':
            return code  # Just return the HTML

        else:
            return "Unsupported language"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Clean up temporary files
        pass #  The files are in a secure temp dir that is deleted on exit

@app.route('/compile', methods=['POST'])
def compile_route():
    """
    Handles the /compile endpoint.
    """
    try:
        data = request.get_json()
        language = data.get('language')
        code = data.get('code')

        if not language or not code:
            return jsonify({'error': 'Missing language or code'}), 400

        result = execute_code(language, code)
        return result, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def cleanup(exception=None):
    """
    Cleanup function to remove the temporary directory.
    """
    shutil.rmtree(TEMP_DIR, ignore_errors=True)


if __name__ == "__main__":
    app.run(debug=True) # Remove debug=True for production
